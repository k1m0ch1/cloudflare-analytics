# Cloudflare Analytics

I just effing annoyed with the metric retention in cloudflare, and the data is actually depend plan you are using, I know cloudflare have graphql so you could get all the metric all you want (within you pricing plan), but I want to make it simple, you see when you get to Web Analytics or Traffic menu in cloudpeler that the data what I want to take it, so this library is just simply imitate what the dashboard cloudpeler do.

## How to Install

`pip install cfanalytics`

and to use

```
from cfanalytics import Auth

cf = Auth(CF_API_KEY, CF_API_EMAIL)
zone = cf.Account(CF_ACCOUNT_ID).Zone(CF_ZONE_ID)

# Here is the available function

# to get all A and CNAME records
getDNSRecord = zone.get_dns_records()

# Data Overview
getDataOverview = zone.get_overview()

# Domain plan
getDomainPlan = zone.get_domain_plan()

# Web Analytics 
# by default it will take 32 days ago from today
getWebAnalytics = zone.get_web_analytics()

# HTTP Traffic
# by default it will take 32 days ago from today
# This only available for Business plan
getHttpTraffics = zone.get_traffics()

```

## License

This Project is licensed under the GNU Affero General Public License v3 (AGPL v3)
See the [LICENSE](LICENSE) file for details
