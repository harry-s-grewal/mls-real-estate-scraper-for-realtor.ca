""" Wrapper the queries module to get property data from realtor.ca. """
from time import sleep
from math import ceil
import os
from random import randint
from requests import HTTPError
import pandas as pd
from queries import get_coordinates, get_property_list, get_property_details

def save_to_file(filename, results):
    """ Saves data to a file. """
    
    results_df = pd.DataFrame()
    for json in results:
        results_df = results_df.append(pd.json_normalize(json))
    if os.path.exists(filename):
        file_df = pd.read_csv(filename)
        file_df = file_df.append(results_df)
        file_df.to_csv(filename, index=False)
    else:
        results_df.to_csv(filename, index=False)


def get_property_list_by_city(city):
    """ Gets a list of properties for a given city, and returns it as a CSV file. """

    coords = get_coordinates(city)  # Creates bounding box for city
    max_pages = 1
    current_page = 1
    while current_page <= max_pages:
        ## Check if property list file already exists.
        ## If it does, use last queried page to set what page should be queried.
        ## Consider keeping all property information within one file.
        try:
            data = get_property_list(
                coords[0], coords[1], 
                coords[2], coords[3],
                current_page=current_page)
            max_pages = ceil(data["Paging"]["TotalRecords"]/data["Paging"]["RecordsPerPage"])
            filename = city.replace(" ", "").replace(",", "") + ".csv"
            save_to_file(filename, data["Results"])
            current_page += 1
            sleep(randint(600, 900))  # sleep 10-15 minutes to avoid rate-limit
        except HTTPError:
            print("Error: " + city)
            sleep(randint(3000, 3600))  # sleep for 50-60 minutes if limited


def get_property_details_from_csv(filename):
    """ Gets the details of a list of properties from the CSV file created by the function above. """

    results_df = pd.read_csv(filename)
    for _, row in results_df.iterrows():
        ## Check if property details file already exists.
        ## If it does, only query for properties that haven't been searched for yet.
        ## Consider keeping all property information within one file.
        property_id = str(row["Id"])
        mls_reference_number = str(row["MlsNumber"])
        try:
            data = get_property_details(property_id, mls_reference_number)
            filename = filename + "Details" + ".csv"
            save_to_file(filename, [data])
            sleep(randint(600, 900))  # sleep 10-15 minutes to avoid rate-limit
        except HTTPError:
            print("Error: " + property_id)
            sleep(randint(3000, 3600))  # sleep for 50-60 minutes if limited