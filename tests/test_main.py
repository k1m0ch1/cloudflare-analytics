import unittest
import os
from cfanalytics import Zone
from dotenv import load_dotenv
import datetime 

load_dotenv()

CF_API_KEY=os.getenv("CF_API_KEY")
CF_HEADER_EMAIL=os.getenv("CF_HEADER_EMAIL")
CF_ZONE_ID=os.getenv("CF_ZONE_ID")

class TestMain(unittest.TestCase):
    def setUp(self):
        self.cf = Zone(CF_API_KEY, CF_HEADER_EMAIL, CF_ZONE_ID)

    def test_get_dns_records(self):
        records = self.cf.get_dns_records()
        self.assertIsInstance(records, list)

    def test_get_domain_plan(self):
        plan = self.cf.get_domain_plan()
        self.assertIsInstance(plan, str)

    def test_get_analytics(self):
        anal = self.cf.get_analytics()
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
