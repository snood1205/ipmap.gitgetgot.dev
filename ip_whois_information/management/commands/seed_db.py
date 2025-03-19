from ipaddress import IPv4Address, AddressValueError
from django.core.management.base import BaseCommand

from ip_whois_information.rdap_client import RDapClient


class Command(BaseCommand):
    help = "Seed the database with currently accurate information"

    def __init__(self):
        super().__init__()
        self.rdap_client = RDapClient()
        self.end_ip = IPv4Address("0.255.255.255")

    def handle(self, *args, **kwargs):
        while self.end_ip <= IPv4Address("255.255.255.255"):
            self.__fetch_next_rdap()

    def __fetch_next_rdap(self):
        try:
            start_address = self.end_ip + 1
            self.stdout.write(self.style.NOTICE(f"Populating from {start_address}"))
            self.end_ip = IPv4Address(self.rdap_client.fetch_rdap(start_address).end_ip)
        except AddressValueError:
            self.stdout.write(
                self.style.SUCCESS("All addresses populated. Good to go!")
            )
