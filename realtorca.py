import requests, json
import pandas as pd
import math
from time import sleep
from random import randint

def getCoordinates(city):
    url = "https://nominatim.openstreetmap.org/search?q=" + city + "&format=json&country=Canada"
    response = requests.get(url=url)
    response.raise_for_status()
    data = response.json()
    for response in data:
        if response["class"] == "boundary" and response["type"] == "administrative":
            return response["boundingbox"] # [latMin, latMax, lonMin, lonMax]
    return data

def sendPropertyListQuery(latMin, latMax, longMin, longMax, priceMin=0, priceMax=10000000, recordsPerPage=200, cultureId=1, currentPage=1, applicationId=1):
    url = "https://api2.realtor.ca/Listing.svc/PropertySearch_Post"
    headers = {"Referer": "https://www.realtor.ca/",
                "Origin": "https://www.realtor.ca/",
                "Host": "api2.realtor.ca"}
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
    response = requests.post(url=url, headers=headers, data=form)
    if response.status_code == 403:
        print("Error 403: Rate limited")
    elif response.status_code != 200:
        print("Error " + str(response.status_code))
    response.raise_for_status()
    return response.json()

def getPropertyListByCity(city):
    coords = getCoordinates(city) # Creates bounding box for city
    maxPages = 1
    currentPage = 1
    results = []
    while currentPage <= maxPages:
        try:
            data = sendPropertyListQuery(coords[0], coords[1], coords[2], coords[3], currentPage=currentPage)
            maxPages = math.ceil(data["Paging"]["TotalRecords"]/data["Paging"]["RecordsPerPage"])
            results.append(data["Results"])
            currentPage += 1
            sleep(randint(600,900)) # sleep for 10-15 minutes to avoid rate-limiting
        except:
            print("Error: " + city)
            sleep(randint(3000,3600)) # sleep for 50-60 minutes if frozen out
    return results

def saveResultsToCSV(city):
    df = pd.DataFrame()
    propertiesList = getPropertyListByCity(city)
    for json in propertiesList:
        df = df.append(pd.json_normalize(json))
    filename = city.replace(" ","").replace(",","") + ".csv"
    df.to_csv(filename)