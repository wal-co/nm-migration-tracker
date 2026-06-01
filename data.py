from datetime import datetime

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
    hist_data = []
    # loop through months 1 = jan
    for i in range(1, 13):
        print(f"Getting month {i}")
        obs = client.get_historic_observations(year, i, 15)
        print(f"Obs month {i}: {obs}")
        hist_data.extend(obs)
    return hist_data

