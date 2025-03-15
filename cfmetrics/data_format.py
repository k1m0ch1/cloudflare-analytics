
def model(dataResult, dataSource):

    dataCompiled = {"by_date":{"date_lists": [], "dates": []}, 
                    "by_domain": {"domain_lists": [], "domains": []}}

    if not hasattr(dataResult, "json"):
        raise ValueError("Expected dataResult to have a .json() method")

    dataMetric = dataResult.json()["data"]["viewer"]["zones" if dataSource == "traffic" else "accounts"][0]["series"]
    for item in dataMetric:
        
        if dataSource == "traffic":
            metricsData = {
                "page_views": item["count"],
                "requests": item["sum"]["visits"],
                "data_transfer_bytes": item["sum"]["edgeResponseBytes"],
                #"error_counts": 0
            }
            source = "zones"
        elif dataSource == "rum":
            metricsData = {
                "page_views": item["count"],
                "visits": item["sum"]["visits"]
            }
            source = "accounts"

        ts = item["dimensions"]["ts"]
        domainName = item["dimensions"]["host"]

        if ts not in dataCompiled["by_date"]["date_lists"]:
            dataCompiled["by_date"]["dates"].append({
                    "date": ts,
                    "domains": [],
                    "domain_lists": []
            })
            dataCompiled["by_date"]["date_lists"].append(ts)
                
        currDateIndex = dataCompiled["by_date"]["date_lists"].index(ts)

        if domainName not in dataCompiled["by_date"]["dates"][currDateIndex]["domain_lists"]:
            dataCompiled["by_date"]["dates"][currDateIndex]["domain_lists"].append(domainName)
            dataCompiled["by_date"]["dates"][currDateIndex]["domains"].append({
                "name": domainName,
                "metrics": metricsData 
            })

        if domainName not in dataCompiled["by_domain"]["domain_lists"]:
            dataCompiled["by_domain"]["domains"].append({
                    "name": domainName,
                    "dates": [],
                    "date_lists": []
            })
            dataCompiled["by_domain"]["domain_lists"].append(domainName)

        currDomainIndex = dataCompiled["by_domain"]["domain_lists"].index(domainName)

        if ts not in dataCompiled["by_domain"]["domains"][currDomainIndex]["date_lists"]:
            dataCompiled["by_domain"]["domains"][currDomainIndex]["date_lists"].append(ts)
            dataCompiled["by_domain"]["domains"][currDomainIndex]["dates"].append({
                "date": ts,
                "metrics": metricsData
            })


    return dataCompiled


