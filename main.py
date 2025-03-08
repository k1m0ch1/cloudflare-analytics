import requests
from dotenv import load_dotenv
import tqdm
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
    "X-AUTH-EMAIL": CF_HEADER_EMAIL,
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
    """Fetch the plan details for a specific domain (zone)."""
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

    default = {
        "requests": 0,
        "page_views": 0,
        "visits": 0,
        "data_transfer_bytes": 0,
        "failure_count": 0,
        "error_count": 0
    }

    start = "2025-02-08T00:00:00Z"
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
                            __typename
                            }
                        sum {
                            edgeResponseBytes # data transfer
                            visits # visit
                            __typename
                            }
                        dimensions {
                            metric: clientRequestHTTPHost
                            ts: date # datetimeFifteenMinutes
                            __typename
                            }
                        __typename
                        }
                    __typename
                    }
                __typename
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

    import pdb; pdb.set_trace()


    

if __name__ == "__main__":
    main()

