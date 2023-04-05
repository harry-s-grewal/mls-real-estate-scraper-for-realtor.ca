""" Wrapper the queries module to get property data from realtor.ca. """
from time import sleep
from math import ceil
import os
from random import randint
from requests import HTTPError
import pandas as pd
from queries import get_coordinates, get_property_list, get_property_details

def get_property_list_by_city(city):
    """ Gets a list of properties for a given city, and returns it as a CSV file. """

    coords = get_coordinates(city)  # Creates bounding box for city
    max_pages = 1
    current_page = 1
    filename = city.replace(" ", "").replace(",", "") + ".csv"
    if os.path.exists(filename):
        results_df = pd.read_csv(filename)
        ## If the queries were interrupted, this will resume from the last page
        current_page = ceil(results_df.shape[0]/200) + 1
        max_pages = current_page + 1
    else:
        results_df = pd.DataFrame()
    while current_page <= max_pages:
        try:
            data = get_property_list(
                coords[0], coords[1], 
                coords[2], coords[3],
                current_page=current_page)
            ## Rounds up the total records by the records per page to nearest int
            max_pages = ceil(data["Paging"]["TotalRecords"]/data["Paging"]["RecordsPerPage"])
            for json in data["Results"]:
                results_df = results_df.append(pd.json_normalize(json))
            results_df.to_csv(filename, index=False)
            current_page += 1
            sleep(randint(600, 900))  # sleep 10-15 minutes to avoid rate-limit
        except HTTPError:
            print("Error occurred on city: " + city)
            sleep(randint(3000, 3600))  # sleep for 50-60 minutes if limited


def get_property_details_from_csv(filename):
    """ Gets the details of a list of properties from the CSV file created above. """

    results_df = pd.read_csv(filename)
    if "HasDetails" not in results_df.columns:
        results_df["HasDetails"] = 0
    for _, row in results_df.iterrows():
        if row["HasDetails"] == 1: # Avoids re-querying properties that already have details
            continue
        property_id = str(row["Id"])
        mls_reference_number = str(row["MlsNumber"])
        try:
            data = get_property_details(property_id, mls_reference_number)
            merged = results_df.join(pd.json_normalize([data, {"HasDetails":1}]), lsuffix='_')
            merged.to_csv(filename, index=False)
            sleep(randint(600, 900))  # sleep 10-15 minutes to avoid rate-limit
        except HTTPError:
            print("Error occurred on propertyID: " + property_id)
            sleep(randint(3000, 3600))  # sleep for 50-60 minutes if limited