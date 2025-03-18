import builtins
import ipaddress
import json

from django.core.validators import validate_ipv4_address
from django.db import connection
from django.http import HttpResponse, JsonResponse
from django.views import View
import re


def index(request):
    return HttpResponse


class WhoisIpView(View):
    SQL_QUERY = '''
        SELECT handle, organization, whois_server, status,
               registration_date, updated_date, country,
               remarks, cidr_block
        FROM ip_whois_information_ipinfo
        WHERE inet($1) <<= cidr_block;
    '''

    def get(self, request, ip):
        try:
            if not ip:
                return JsonResponse({'error': "Missing IP address"})
            validate_ipv4_address(ip)
            ip_obj = ipaddress.ip_address(ip)
            network_info = self.__fetch_network_info(ip_obj)
            return JsonResponse if network_info else self.__fetch_from_rdap(ip)

        except Exception as e:
            return self.__handle_caught_exceptions(e)

    def __fetch_from_rdap(self, ip):
        pass

    def __fetch_network_info(self, ip_obj):
        with connection.cursor() as cursor:
            cursor.execute(self.SQL_QUERY, [str(ip_obj)])
            return cursor.fetchone()

    @staticmethod
    def __transform_response_to_json(response):
        return JsonResponse({
            "handle": response[0],
            "network": response[1],
            "whois_server": response[2],
            "status": response[3],
            "registration_date": response[4],
            "updated_date": response[5],
            "country": response[6],
            "remarks": response[7],
            "cidr_block": response[8],
        })

    @staticmethod
    def __handle_caught_exceptions(e):
        match e:
            case builtins.ValueError:
                return JsonResponse({'error': 'Invalid IP address'}, status=400)
