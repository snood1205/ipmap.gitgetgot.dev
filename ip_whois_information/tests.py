from unittest.mock import patch, MagicMock
from django.test import TestCase
from ip_whois_information.models import IPInfo
from ip_whois_information.rdap_client import RDapClient


class IPInfoModelTest(TestCase):
    def setUp(self):
        self.ip_info = IPInfo.objects.create(
            handle="1.1.1.0 - 1.1.1.255",
            whois_server="whois.apnic.net",
            organization="APNIC-LABS",
            network_type="ASSIGNED PORTABLE",
            status="active",
            registration_date="2011-08-10",
            updated_date="2023-04-26",
            country="AU",
            ref_url="https://rdap.apnic.net/ip/1.0.0.0/24",
            remarks=[
                [
                    "APNIC and Cloudflare DNS Resolver project",
                    "Routed globally by AS13335/Cloudflare",
                    "Research prefix for APNIC Labs",
                ],
                [
                    "---------------",
                    "All Cloudflare abuse reporting can be done via",
                    "resolver-abuse@cloudflare.com",
                    "---------------",
                ],
            ],
            start_ip="1.0.0.0",
            end_ip="1.0.0.255",
        )

    def test_ipinfo_str(self):
        self.assertEqual(str(self.ip_info), "APNIC-LABS (1.1.1.0 - 1.1.1.255)")

    def test_ipinfo_as_dict(self):
        data = self.ip_info.as_dict()
        self.assertEqual(data["handle"], "1.1.1.0 - 1.1.1.255")
        self.assertEqual(data["whois_server"], "whois.apnic.net")
        self.assertEqual(data["organization"], "APNIC-LABS")
        self.assertEqual(data["network_type"], "ASSIGNED PORTABLE")
        self.assertEqual(data["status"], "active")
        self.assertEqual(data["registration_date"], "2011-08-10")
        self.assertEqual(data["updated_date"], "2023-04-26")
        self.assertEqual(data["country"], "AU")


class RDapClientTest(TestCase):
    @patch("ip_whois_information.rdap_client.get")
    def test_fetch_rdap(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "handle": "1.1.1.0 - 1.1.1.255",
            "whois_server": "whois.apnic.net",
            "organization": "APNIC-LABS",
            "network_type": "ASSIGNED PORTABLE",
            "status": "active",
            "registration_date": "2011-08-10",
            "updated_date": "2023-04-26",
            "country": "AU",
        }
        mock_get.return_value = mock_response

        rdap_data = RDapClient.fetch_rdap("1.1.1.1")
        self.assertEqual(rdap_data.handle, "1.1.1.0 - 1.1.1.255")
        self.assertEqual(rdap_data.whois_server, "whois.apnic.net")
        self.assertEqual(rdap_data.organization, "APNIC-LABS")
        self.assertEqual(rdap_data.network_type, "ASSIGNED PORTABLE")
        self.assertEqual(rdap_data.status, "active")
        self.assertEqual(rdap_data.registration_date, "2011-08-10")
        self.assertEqual(rdap_data.updated_date, "2023-04-26")
        self.assertEqual(rdap_data.country, "AU")
