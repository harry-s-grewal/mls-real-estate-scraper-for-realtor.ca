""" Wrapper the queries module to get property data from realtor.ca. """
from time import sleep
from math import ceil
from random import randint
from requests import HTTPError
import pandas as pd
from queries import get_coordinates, get_property_list, get_property_details


def get_property_list_by_city(city):
    """ Gets a list of properties for a given city, and returns it as a CSV file. """
    coords = get_coordinates(city)  # Creates bounding box for city
    max_pages = 1
    current_page = 1
    results = []
    while current_page <= max_pages:
        try:
            data = get_property_list(
                coords[0], coords[1], 
                coords[2], coords[3],
                current_page=current_page)
            max_pages = ceil(data["Paging"]["TotalRecords"]/data["Paging"]["RecordsPerPage"])
            results.append(data["Results"])
            current_page += 1
            sleep(randint(600, 900))  # sleep 10-15 minutes to avoid rate-limit
        except HTTPError:
            print("Error: " + city)
            sleep(randint(3000, 3600))  # sleep for 50-60 minutes if limited
    results_df = pd.DataFrame()
    for json in results:
        results_df = results_df.append(pd.json_normalize(json))
    filename = city.replace(" ", "").replace(",", "") + ".csv"
    results_df.to_csv(filename)


def get_property_details_from_csv(filename):
    """ Gets the details of a list of properties from the CSV file created by the function above. """
    results = []
    results_df = pd.read_csv(filename)
    for _, row in results_df.iterrows():
        property_id = str(row["Id"])
        mls_reference_number = str(row["MlsNumber"])
        try:
            data = get_property_details(property_id, mls_reference_number)
            results.append(data["Results"])
            sleep(randint(600, 900))  # sleep 10-15 minutes to avoid rate-limit
        except HTTPError:
            print("Error: " + property_id)
            sleep(randint(3000, 3600))  # sleep for 50-60 minutes if limited
    results_df = pd.DataFrame()
    for json in results:
        results_df = results_df.append(pd.DataFrame.from_dict(json))
    filename = filename + "Details" + ".csv"
    results_df.to_csv(filename)

# 3. Create a readme file to explain how to use the script