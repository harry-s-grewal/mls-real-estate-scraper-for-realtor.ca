import requests, json
import math

url = "https://api2.realtor.ca/Listing.svc/PropertySearch_Post"
headers = {"Referer": "https://www.realtor.ca/",
               "Origin": "https://www.realtor.ca/",
               "Host": "api2.realtor.ca"}

def getCoordinates(city):
    url = "https://nominatim.openstreetmap.org/search?q=" + city + "&format=json&country=Canada"
    response = requests.get(url=url)
    response.raise_for_status()
    data = response.json()
    for response in data:
        if response["class"] == "boundary" and response["type"] == "administrative":
            return response["boundingbox"] # [latMin, latMax, lonMin, lonMax]
    return data

def makeForm(latMin, latMax, longMin, longMax, priceMin=0, priceMax=10000000, recordsPerPage=200, cultureId=1, currentPage=1, applicationId=1):
    form = {
        "LatitudeMin": latMin,
        "LatitudeMax": latMax,
        "LongitudeMin": longMin,
        "LongitudeMax": longMax,
        "PriceMin": priceMin,
        "PriceMax": priceMax,
        "RecordsPerPage": recordsPerPage,
        "CultureId": cultureId,
        "CurrentPage": currentPage,
        "ApplicationId": applicationId
    }
    return form

def getProperties(city):
    coords = getCoordinates(city)
    maxPages = 1
    currentPage = 1
    results = []
    while currentPage <= maxPages:
        form = makeForm(coords[0], coords[1], coords[2], coords[3], currentPage=currentPage)
        response = requests.post(url=url, headers=headers, data=form)
        response.raise_for_status()
        data = response.json()
        maxPages = math.ceil(data["Paging"]["TotalRecords"]/data["Paging"]["RecordsPerPage"])
        results.append(data["Results"])
        currentPage += 1
    return results

import pandas as pd
df = pd.DataFrame()
propertiesList = getProperties("Victoria, BC")
for json in propertiesList:
    df = df.append(pd.json_normalize(json))
df.to_csv("properties.csv")