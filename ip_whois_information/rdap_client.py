from django.core.validators import validate_ipv4_address
from requests import get
from ip_whois_information.models import IPInfo


class RDapClient:
    @classmethod
    def fetch_rdap(cls, ip_address):
        validate_ipv4_address(ip_address)
        url = f"https://rdap.org/ip/{ip_address}"
        json_response = get(url).json()
        ip_info = cls.__create_ip_info_from_json_response(json_response)
        ip_info.save()
        return ip_info

    @staticmethod
    def __create_ip_info_from_json_response(json_response):
        cidr0_cidr = json_response.get("cidr0_cidrs")[0]
        cidr_block = f"{cidr0_cidr['v4prefix']}/{cidr0_cidr['length']}"
        return IPInfo(
            handle=json_response.get("handle"),
            whois_server=json_response.get("port43"),
            organization=json_response.get("name"),
            network_type=json_response.get("type"),
            status=",".join(json_response.get("status")),
            registration_date=next(
                (
                    event["eventDate"][:10]
                    for event in json_response.get("events")
                    if event["eventAction"] == "registration"
                ),
                None,
            ),
            updated_date=next(
                (
                    event["eventDate"][:10]
                    for event in json_response.get("events")
                    if event["eventAction"] == "last changed"
                ),
                None,
            ),
            country=json_response.get("country"),
            ref_url=next(
                (
                    link["href"]
                    for link in json_response.get("links")
                    if link["rel"] == "self"
                ),
                "",
            ),
            remarks=[remark["description"] for remark in json_response.get("remarks")],
            cidr_block=cidr_block,
        )
