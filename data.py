import time
import json
import os
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor

CACHE_FILE = "cache/observations.json"
CACHE_EXPIRY_HOURS = 24

def get_cached_observations(client, year=2025):
    # if CACHE_FILE exists and is fresh, return cached data
    if os.path.exists(CACHE_FILE):
        # check time
        modified_time = datetime.fromtimestamp(os.path.getmtime(CACHE_FILE))
        if datetime.now() - modified_time < timedelta(hours=24):
            # cache is fresh — read and return it
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
    # otherwise fetch fresh data, save, and return
    data = get_yearly_observations(client, year)
    os.makedirs("cache", exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump(data, f)

    return data

def build_presence_matrix(observations):
    matrix = {}
    for obs in observations:
        #get the species name from comName
        species = obs["comName"]
        # get the month from obsDT
        month = datetime.fromisoformat(obs["obsDt"]).month
        # add the month to matrix[species] if not already there
        if species not in matrix:
            matrix[species] = [month]
        else:
            if month not in matrix[species]:
                matrix[species].append(month)
    return matrix

def sort_matrix(matrix):
    # Sort months of species matrix
    for species, months in matrix.items():
        months.sort()
    return matrix

def get_yearly_observations(client, year=2025):
    start = time.time()
    hist_data = []
    # loop through months and fetch data
    fetch_month = lambda month: client.get_historic_observations(year, month, 15)
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(fetch_month, range(1, 13)))
    hist_data = [obs for month_results in results for obs in month_results]
    print(f"Fetched in {time.time() - start:.2f}s")
    return hist_data

