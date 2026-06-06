import time
import json
import os
from models import Bird
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor

CACHE_FILE = "cache/observations.json"
TAXONOMY_CACHE_FILE = "cache/taxonomy.json"
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

def get_cached_taxonomy(client):
    if os.path.exists(TAXONOMY_CACHE_FILE):
        modified_time = datetime.fromtimestamp(os.path.getmtime(TAXONOMY_CACHE_FILE))
        # Cache life = 30 days
        if datetime.now() - modified_time < timedelta(days=30):
            with open(TAXONOMY_CACHE_FILE, "r") as f:
                return json.load(f)

    taxonomy = client.get_taxonomy()
    os.makedirs("cache", exist_ok=True)
    with open(TAXONOMY_CACHE_FILE, "w") as f:
        json.dump(taxonomy, f)
    return taxonomy

def build_presence_matrix(observations, taxonomy_lookup):
    matrix = {}
    for obs in observations:
        #get the species name from comName
        species = obs["comName"]
        # get the month from obsDT
        month = datetime.fromisoformat(obs["obsDt"]).month
        # add the Bird obj to matrix[species] if not already there
        if species not in matrix:
            matrix[species] = Bird(
                    obs,
                    taxonomy_lookup
                )
        matrix[species].add_months_seen(month)
    return matrix

def sort_matrix(matrix):
    # Sort months of species matrix
    for species, bird in matrix.items():
        bird.months.sort()
    return matrix

def get_yearly_observations(client, year=2025):
    start = time.time()
    hist_data = []
    # loop through months and fetch data
    fetch_month = lambda month: client.get_historic_observations(year, month, 15)
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(fetch_month, range(1, 13)))
    hist_data = [obs for month_results in results for obs in month_results]
    # print(f"Fetched in {time.time() - start:.2f}s")
    return hist_data

def build_taxonomy_lookup(client):
    taxonomy = get_cached_taxonomy(client)
    return {t["speciesCode"]: t.get("familyComName", "Unknown") for t in taxonomy}
