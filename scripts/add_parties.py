# This script adds party information to the merged battleground senate data CSV file. It uses the FEC API to get the party information for each candidate in the merged data.
import pandas as pd
import requests
import time

API_KEY = "LD7dMKPmMfdghqDTQTMkcWGbNC8Pcp8qLJzGWGgM"  # Replace with your actual FEC API key. I'm not giving you mine :).
BASE_URL = "https://api.open.fec.gov/v1" 

master_df = pd.read_csv("merged_battleground_senate_data.csv")

unique_committees = master_df["committee_id"].dropna().unique().tolist()
print(f"Found {len(unique_committees)} unique committees to process.")

committee_party_map = {}

print("Fetching party information for each committee from the FEC...")
for i in range(0, len(unique_committees), 50):
    batch = unique_committees[i:i+50]
    
    params = {
        "api_key": API_KEY,
        "committee_id": batch,
        "per_page": 100
    }
    
    response = requests.get(f"{BASE_URL}/committees/", params=params)
    if response.status_code == 200:
        results = response.json().get("results", [])
        for committee in results:
            c_id = committee.get("committee_id")
            party_code = committee.get("party")
            if party_code == "DEM":
                party_name = "Democratic"
            elif party_code == "REP":
                party_name = "Republican"
            else:
                party_name = "Other"

            committee_party_map[c_id] = party_name
            
    time.sleep(1)  # Sleep to avoid hitting the API rate limit

master_df["committee_party"] = master_df["committee_id"].map(committee_party_map)

master_df["committee_party"] = master_df["committee_party"].fillna("Unknown")

final_output = "final_battleground_senate_audit.csv"
master_df.to_csv(final_output, index=False)

print(f"Party information added and saved to {final_output}.")
print(master_df["committee_party"].value_counts())
print("Script completed successfully.")
