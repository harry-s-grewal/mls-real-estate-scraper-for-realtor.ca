# Realtor.ca API Wrapper and Scraper
Python wrapper and scraper for the Realtor.ca website. Use it to scrape Canadian real-estate listings easily.

## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the package requirements.

```bash
pip -r requirements.txt
```

## Context
Realtor.ca has two API endpoints: `PropertySearch_Post` and `PropertyDetails`. Querying `PropertySearch_Post` 
will return a list of properties in a .json format, including some limited details. Querying `PropertyDetails` will provide detailed information on each property. Depending on what you're looking for, you can query one or the other, but be aware that getting details on each property is slow. That's because Realtor.ca is rate limited (boo). If you make too many queries too often, you'll receive an `Error 403: Unauthorized` error. It's not clear what the rate limit is, but waiting an hour or so between limits stops the freeze-out.

## Usage
In `queries.py` you will find queries to Realtor.ca for both the `PropertySearch_Post` endpoint and the `PropertyDetails` endpoint. It also contains a query to get the coordinate bounding box of a city, as that's what Realtor.ca uses to determine which properties to list.

In `realtorca.py` there are two functions to automate the scraping of Realtor.ca.

`get_property_list_by_city()` will scrape a list of properties by city and save it as a .csv.
```python
get_property_list_by_city("Calgary, AB")
```

Result:
```bash
CalgaryAB.csv
```
`get_property_details_from_csv()` will use that .csv file to get detailed property listings.
```python
get_property_list_by_city("CalgaryAB.csv")
```

Result:
```bash
CalgaryABDetails.csv
```


Follows PEP8 Styleguide.
