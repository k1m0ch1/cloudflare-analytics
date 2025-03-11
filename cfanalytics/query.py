
from datetime import datetime, timedelta


def query_zone_overview(zone_id: str, start_date=(datetime.now()-timedelta(seconds=2764800)).strftime("%Y-%m-%d"), end_date=datetime.now().strftime("%Y-%m-%d")):

    try:
        start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid date format. Expected format: YYYY-MM-DD")

    threshold_date = datetime.utcnow() - timedelta(seconds=2764800)

    queryBody = {
        "query": """
            query GetZoneAnalytics($zoneTag: string){
                viewer{
                    zones(filter: {zoneTag: $zoneTag}){
                        # Total Unique Visitors
                        totals: httpRequests1dGroups(limit: 10000, filter: {date_geq: $start_date, date_lt: $end_date}){
                            uniq{
                                uniques
                            }
                        }

                        # Zone Analytics by Timeslot
                        zones: httpRequests1dGroups(orderBy:[date_ASC], limit: 10000, filter: {date_geq: $start_date, date_lt: $end_date}){
                            dimensions{
                                timeslot: date
                            }
                            uniq{
                                uniques
                            }
                            sum{

                                # Browser Statistics
                                browserMap{
                                    pageViews
                                    key: uaBrowserFamily
                                }
                                
                                # Data Transfer Statistics
                                bytes
                                cachedBytes
                                cachedRequests

                                contentTypeMap {
                                    bytes
                                    key: edgeResponseContentTypeName
                                }

                                # Traffic by Country
                                countryMap {
                                    bytes
                                    requests 
                                    threats
                                    key: clientCountryName
                                }
                                
                                pageViews
                                requests

                                #Response Status Breakdown
                                responseStatusMap {
                                    requests
                                    key: edgeResponseStatus
                                }

                                # Threat Metrics
                                threats
                                threatPathingMap {
                                    requests
                                    key: threatPathingName
                                }
                            }
                        }
                    }
                }
            }
            """,
        "variables":{
            "zoneTag": zone_id,
            "start_date": start_date,
            "end_date": end_date
            }
        }

    return queryBody

    
    

