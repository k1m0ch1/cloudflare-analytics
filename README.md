# Cloudflare Analytics 

I just hate it when cloudpler have a limitation with the data and I need to login whenever I want to see the metric, its beautifully designed with cloudflare, but I just need a simple data like requests and threat, so I plan to made this library to handle GraphQL cloudflare metric so I could store the metric for ever.

## 🚀 Features 

- 📊 Pulls data straight from Cloudflare's GraphQL API 
- 🔍 Gives you traffic insights, some of the data depend with pricing plan 
- 📈 Shows threats metrics
- ⚡ Lightweight, just like your trust in Cloudflare’s analytics

## 📦 Installation 

Clone this glorified data-fetcher and install some dependencies:

```sh
pip install cfmetrics
```

## 🔧 Configuration 

you need the Cloudflare API Key and Registerd Email for API Key, the permission needs to create is:

1. Zone Read Analytics

2. Zone Read DNS 

3. Account Read Analytics

## 🚀 Usage Cloudflare 

```
from cfmetrics import Auth

cf= Auth(CF_APIKEY, CF_EMAIL)
zone = cf.Account(CF_ACCOUNTID).Zone(CF_ZONEID)

# and here is the available function

# get all A and CNAME Record
getDNSRecord = zone.get_dns_records()

# get Data Overview
getDataOverview = zone.get_overview()

# Domain plan
getDomainPlan = zone.get_domain_plan()

# Web Analytics
getWebAnalytics = zone.get_web_analytics()

# HTTP traffic
# This only available for Business plan
getHttpTraffics = zone.get_traffics()

```

## 🛠 API Reference 

This tool "leverages" Cloudflare’s GraphQL API, which you can tweak in `analytics.py`. Or just pretend you understand GraphQL by checking out [Cloudflare’s GraphQL API Docs](https://developers.cloudflare.com/graphql/).

## 📜 License 

This project is licensed under the MIT License—so do whatever you want with it. 

## 🤝 Contributing

Want to make this better? Great! Open an issue, submit a pull request, or just scream into the void.

## 📬 Contact 

Got questions, complaints, or just need someone to blame? Reach out to [@k1m0ch1](https://github.com/k1m0ch1) or open an issue. 

---

🚀 **Cloudflare Analytics – Because Staring at Graphs Makes You Feel Productive!**

