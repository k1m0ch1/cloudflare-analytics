import unittest
import os
from cfmetrics import Auth
from dotenv import load_dotenv
import datetime 
import json

load_dotenv()

CF_API_KEY=os.getenv("CF_API_KEY")
CF_HEADER_EMAIL=os.getenv("CF_HEADER_EMAIL")
CF_ZONE_ID=os.getenv("CF_ZONE_ID")
CF_ACCOUNT_ID=os.getenv("CF_ACCOUNT_ID")

class TrafficProcessor:
    def __init__(self, mock_file):
        self.mock_file = mock_file
        self.data = self.load_mock_data()
    
    def load_mock_data(self):
        with open(self.mock_file, 'r') as f:
            return json.load(f)
    
    def get_traffic_by_date(self, date):
        return self.data.get('by_date', {}).get(date, {})
    
    def get_traffic_by_domain(self, domain):
        return self.data.get('by_domain', {}).get(domain, {})
    
    def get_total_page_views(self):
        total_views = 0
        for date, domains in self.data.get('by_date', {}).items():
            for domain, metrics in domains.items():
                total_views += metrics.get('page_views', 0)
        return total_views

class TestMain(unittest.TestCase):

    def setUp(self):
        self.cf = Auth(CF_API_KEY, CF_HEADER_EMAIL)
        self.account = self.cf.Account(CF_ACCOUNT_ID)
        self.zone = self.account.Zone(CF_ZONE_ID)
        self.processor = TrafficProcessor(f"{os.getcwd()}/tests/mock-traffic-rum.json")

    def test_get_dns_records(self):
        records = self.zone.get_dns_records()
        self.assertIsInstance(records, list)

    def test_get_domain_plan(self):
        plan = self.zone.get_domain_plan()
        self.assertIsInstance(plan, str)

    def test_get_traffic_wrong_datetime_format(self):
        # make sure wrong format will return error
        with self.assertRaises(ValueError) as context:
            self.zone.get_traffics("2025-1-07 17:05:52Z", "2025-03-07T17:05:52Z")

        self.assertIn("Invalid date format. Expected format: YYYY-MM-DDTHH:MM:SSZ", str(context.exception))
        
        start_date = "2025-01-07T17:05:52Z"
        with self.assertRaises(ValueError) as context:
            self.zone.get_traffics(start_date, "2025-03-07T17:05:52Z")

        self.assertIn(f"start_date cannot be more than 2,764,800 seconds (32 days) ago. Given: {start_date}", str(context.exception))
        
    def test_get_web_analytics(self):
        anal = self.zone.get_web_analytics()
        self.assertIsInstance(anal, dict)

    def test_get_web_analytics_wrong_datetime_format(self):
        # make sure wrong format will return error
        with self.assertRaises(ValueError) as context:
            self.zone.get_web_analytics("2025-1-07 17:05:52Z", "2025-03-07T17:05:52Z")

        self.assertIn("Invalid date format. Expected format: YYYY-MM-DDTHH:MM:SSZ", str(context.exception))


    def test_get_traffics(self):
        anal = self.zone.get_traffics()
        self.assertIsInstance(anal, dict)

    def test_load_mock_data(self):
        self.assertTrue(self.processor.data, "Mock data should be loaded.")

    def test_get_traffic_by_date(self):
        sample_date = '2025-02-22'
        traffic = self.processor.get_traffic_by_date(sample_date)
        self.assertIsInstance(traffic, dict, "Traffic data should be a dictionary.")
    
    def test_get_traffic_by_domain(self):
        sample_domain = 'saweria.co'
        traffic = self.processor.get_traffic_by_domain(sample_domain)
        self.assertIsInstance(traffic, dict, "Traffic data should be a dictionary.")
    
    def test_total_page_views(self):
        total_views = self.processor.get_total_page_views()
        self.assertGreater(total_views, 0, "Total page views should be greater than 0.")

    def test_get_overview(self):
        anal = self.zone.get_overview()
        self.assertIsInstance(anal, dict)


if __name__ == "__main__":
    unittest.main()
