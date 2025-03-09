import requests
from dotenv import load_dotenv
import tqdm
import sys
import os

load_dotenv()

CF_API_KEY = os.getenv("CF_API_KEY")
CF_HEADER_EMAIL = os.getenv("CF_HEADER_EMAIL")
CF_PLAN=os.getenv("CF_PLAN")
CF_ZONE_ID=os.getenv("CF_ZONE_ID")
CF_GRAPHQL_URL="https://api.cloudflare.com/client/v4/graphql"
CF_API_URL="https://api.cloudflare.com/client/v4"

headerGraphql = {
    "Authorization": f"Bearer {CF_API_KEY}",
}

def get_dns_records(zone_id):
    """Fetch DNS records for a given zone (only A and CNAME records)."""
    url = f"{CF_API_URL}/zones/{zone_id}/dns_records"
    params = {"type": "A"}  # Fetch A records first
    response_a = requests.get(url, headers=headerGraphql, params=params)

    params = {"type": "CNAME"}  # Fetch CNAME records
    response_cname = requests.get(url, headers=headerGraphql, params=params)

    if response_a.status_code == 200 and response_cname.status_code == 200:
        return response_a.json().get("result", []) + response_cname.json().get("result", [])
    else:
        print("Failed to fetch DNS records:", response_a.text, response_cname.text)
        return []

def get_domain_plan(zone_id):
    """
    Get the Domain Liecense or Pricing Plan so it will give a clue about which metric
    that we could actually scrape
    The License most likely FREE/PRO/BUSINESS/ENTERPRISE
    at this moment we only support FREE and BUSINESS
    """

    url = f"{CF_API_URL}/zones/{zone_id}"
    response = requests.get(url, headers=headerGraphql)
    
    if response.status_code == 200:
        zone_info = response.json().get("result", {})
        plan_name = zone_info.get("plan", {}).get("name", "Unknown")
        return plan_name
    else:
        print(f"Failed to fetch plan details for zone {zone_id}:", response.text)
        return "Unknown"


def main():
    
    print(get_domain_plan(CF_ZONE_ID))

    dns_records = [result['name'] for result in get_dns_records(CF_ZONE_ID)]
    listofDomainFilter = [{"clientRequestHTTPHost": item} for item in dns_records]

    start = "2025-01-08T00:00:00Z"
    end = "2025-03-08T23:59:59Z"

    # This query only working for business plan
    queryBody = {
        "query": """
            query VisitsDaily($zoneTag: string, $filter: ZoneHttpRequestsAdaptiveGroupsFilter_InputObject){
                viewer{
                    zones(filter: {zoneTag: $zoneTag}) {
                    series: httpRequestsAdaptiveGroups(limit: 10000, filter: $filter) {
                        count # pageview
                        avg {
                            sampleInterval
                            }
                        sum {
                            edgeResponseBytes # data transfer
                            visits # visit
                            }
                        dimensions {
                            metric: clientRequestHTTPHost
                            ts: date # datetimeFifteenMinutes
                            }
                        }
                    }
                }
            }
                """,
        "variables":{
            "zoneTag": CF_ZONE_ID,
            "filter": {
                "AND": [{
                    "datetime_geq": start,
                    "datetime_leq": end
                }, {
                    "requestSource": "eyeball"
                }, {
                    "AND": [{
                        "edgeResponseStatus": 200,
                        "edgeResponseContentTypeName": "html"
                    }]
                }, {
                    "OR": listofDomainFilter
                }]
            }
        }
    }

    getDataOK = requests.post(CF_GRAPHQL_URL, headers=headerGraphql, json=queryBody)
    if getDataOK.status_code != 200:
        print(f"ERROR {getDataOK.text}")
    dataCompiled = {"by_date":{}, "by_domain": {}}
    try:
        dataMetric = getDataOK.json()["data"]["viewer"]["zones"][0]["series"]
        for item in dataMetric:
            default = {
                "page_views": 0,
                "requests": 0,
                "data_transfer_bytes": 0,
                "error_count": 0
            }            
            ts = item["dimensions"]["ts"]
            domainName = item["dimensions"]["metric"]
            if ts not in dataCompiled["by_date"]:
                dataCompiled["by_date"][ts] = {}
            if domainName not in dataCompiled["by_date"][ts]:
                dataCompiled["by_date"][ts][domainName] = default

            dataCompiled["by_date"][ts][domainName]["page_views"] = item["count"]
            dataCompiled["by_date"][ts][domainName]["requests"] = item["sum"]["visits"]
            dataCompiled["by_date"][ts][domainName]["data_transfer_bytes"] = item["sum"]["edgeResponseBytes"]
            
            if domainName not in dataCompiled["by_domain"]:
                dataCompiled["by_domain"][domainName] = {}
            if ts not in dataCompiled["by_domain"][domainName]:
                dataCompiled["by_domain"][domainName][ts] = default

            dataCompiled["by_domain"][domainName][ts]["page_views"] = item["count"]
            dataCompiled["by_domain"][domainName][ts]["requests"] = item["sum"]["visits"]
            dataCompiled["by_domain"][domainName][ts]["data_transfer_bytes"] = item["sum"]["edgeResponseBytes"]

        queryBody["variables"]["filter"]["AND"][2]["AND"][0]["edgeResponseStatus"] = 500
        getDataFailure = requests.post(CF_GRAPHQL_URL, headers=headerGraphql, json=queryBody)

        if getDataFailure.status_code != 200:
            print("ERROR to GET DATA FAILURE TRAFFIC")
            sys.exit()

        dataError = getDataFailure.json()["data"]["viewer"]["zones"][0]["series"]
        for itemError in dataError:
            ts = itemError["dimensions"]["ts"]
            domainName = itemError["dimensions"]["metric"]
            dataCompiled["by_date"][ts][domainName]["error_count"] = itemError["count"]
            dataCompiled["by_domain"][domainName][ts]["error_count"] = itemError["count"]

    except (KeyError, IndexError, TypeError):
        print("Data is missing or invalid")
    

if __name__ == "__main__":
    main()

