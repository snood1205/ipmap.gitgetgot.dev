import builtins
import ipaddress
import json

from django.core.validators import validate_ipv4_address
from django.db import connection
from django.http import JsonResponse
from django.views import View
import re

from ip_whois_information.rdap_client import RDapClient


class WhoisIpView(View):
    SQL_QUERY = """
        SELECT handle, organization, whois_server, status,
               registration_date, updated_date, country,
               start_ip, end_ip
        FROM ip_whois_information_ipinfo
        WHERE inet(%s) BETWEEN start_ip AND end_ip
    """

    def get(self, request, ip):
        try:
            if not ip:
                return JsonResponse({"error": "Missing IP address"})
            validate_ipv4_address(ip)
            ip_obj = ipaddress.ip_address(ip)
            network_info = self.__fetch_network_info(ip_obj)
            return self.__transform_response_to_json(network_info) if network_info else self.__fetch_from_rdap(ip)

        except Exception as e:
            return JsonResponse({"error": str(e)})

    @classmethod
    def __fetch_from_rdap(cls, ip):
        rdap_data = RDapClient.fetch_rdap(ip)
        if not rdap_data:
            return JsonResponse({"error": "RDAP lookup failed"}, status=404)
        return JsonResponse(rdap_data.as_dict())

    @classmethod
    def __fetch_network_info(cls, ip_obj):
        with connection.cursor() as cursor:
            cursor.execute(cls.SQL_QUERY, [str(ip_obj)])
            return cursor.fetchone()

    @staticmethod
    def __transform_response_to_json(response):
        return JsonResponse(
            {
                "handle": response[0],
                "network": response[1],
                "whois_server": response[2],
                "status": response[3],
                "registration_date": response[4],
                "updated_date": response[5],
                "country": response[6],
                "start_ip": response[7],
                "end_ip": response[8]
            }
        )

    # @staticmethod
    # def __handle_caught_exceptions(e):
    #     match e:
    #         case builtins.ValueError:
    #             return JsonResponse({"error": "Invalid IP address"}, status=400)