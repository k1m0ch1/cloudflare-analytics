import unittest
import os
from cfanalytics import Auth
from dotenv import load_dotenv
import datetime 

load_dotenv()

CF_API_KEY=os.getenv("CF_API_KEY")
CF_HEADER_EMAIL=os.getenv("CF_HEADER_EMAIL")
CF_ZONE_ID=os.getenv("CF_ZONE_ID")
CF_ACCOUNT_ID=os.getenv("CF_ACCOUNT_ID")

class TestMain(unittest.TestCase):

    def setUp(self):
        self.cf = Auth(CF_API_KEY, CF_HEADER_EMAIL)
        self.account = self.cf.Account(CF_ACCOUNT_ID)
        self.zone = self.account.Zone(CF_ZONE_ID)

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
        

    def test_get_traffics(self):
        anal = self.zone.get_traffics()
        self.assertIsInstance(anal, dict)

        self.assertIn("by_date", anal)
        self.assertIn("by_domain", anal)

        # Check "by_date" structure
        self.assertIsInstance(anal["by_date"], dict)
        for date, domains in anal["by_date"].items():
            # Ensure date keys are in valid format
            try:
                datetime.datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                self.fail(f"Invalid date format: {date}")

            # Ensure domains structure
            self.assertIsInstance(domains, dict)
            for domain, metrics in domains.items():
                self.assertIsInstance(domain, str)
                self.assertIsInstance(metrics, dict)
                self.assertIn("page_views", metrics)
                self.assertIn("requests", metrics)
                self.assertIn("data_transfer_bytes", metrics)
                self.assertIn("error_count", metrics)
                self.assertIsInstance(metrics["page_views"], int)
                self.assertIsInstance(metrics["requests"], int)
                self.assertIsInstance(metrics["data_transfer_bytes"], int)
                self.assertIsInstance(metrics["error_count"], int)

        # Check "by_domain" structure
        self.assertIsInstance(anal["by_domain"], dict)
        for domain, dates in anal["by_domain"].items():
            self.assertIsInstance(domain, str)
            self.assertIsInstance(dates, dict)
            for date, metrics in dates.items():
                try:
                    datetime.datetime.strptime(date, "%Y-%m-%d")
                except ValueError:
                    self.fail(f"Invalid date format: {date} in by_domain")

                self.assertIsInstance(metrics, dict)
                self.assertIn("page_views", metrics)
                self.assertIn("requests", metrics)
                self.assertIn("data_transfer_bytes", metrics)
                self.assertIn("error_count", metrics)
                self.assertIsInstance(metrics["page_views"], int)
                self.assertIsInstance(metrics["requests"], int)
                self.assertIsInstance(metrics["data_transfer_bytes"], int)
                self.assertIsInstance(metrics["error_count"], int)



if __name__ == "__main__":
    unittest.main()
