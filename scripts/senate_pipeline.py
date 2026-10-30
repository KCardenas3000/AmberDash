import os
import time
import pandas as pd
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
# We're using the FEC API to get campaign finance data. I took off my API key for security reasons, but go to the api.fec.gov website to get your own for this.
API_KEY = os.getenv("FEC_API_KEY")
BASE_URL = "https://api.open.fec.gov/v1"
CYCLE = "2026" # The election cycle we're interested in and the one we're in right now. You can change this to any cycle you want, but the FEC only has data for 2020 and later.

# We're going to track recent campaign finance reports for every competitive senate race in the cycle. You can change this to whatever races you want.
TARGET_RACES = ["AK", "GA", "IA", "KS", "ME", "MI", "MN", "NE", "NH", "NC", "OH", "SC", "TX"]

def fetch_state_spending(state):
    """Fetches the campaign finance data for a given state from the FEC API."""
    all_records = []
    endpoint = f"{BASE_URL}/schedules/schedule_b/"

    # We're going to restrict the params to the current cycle and the state's we are interested in. The FEC API has a lot of data, so we want to limit it to just what we need.
    params = {
        "api_key": API_KEY,
        "cycle": CYCLE,
        "state": state,
        "office": "S",  # S for Senate races
        "per_page": 100,  # Adjust as needed
    }

    has_more = True
    page = 1

    while has_more:
        print(f"Fetching page {page} for state {state}...")
        response = requests.get(endpoint, params=params)

        if response.status_code != 200:
            print(f"Error fetching data for state {state}: {response.status_code}")
            break
        try:
            data = response.json()
        except Exception:
            print("\nCRITICAL ERROR: Server blocked the request. Inspecting the response content for more details...")
            print("-"* 50)
            print(response.text[:500])  # Print the first 500 characters of the response for debugging
            print("-"* 50)
            break

        results = data.get("results", [])
        all_records.extend(results)

        # FEC API deep pagination: check if there's more data to fetch
        pagination = data.get("pagination", {})
        last_index = pagination.get("last_index")
        if last_index and len(results) > 0:
            params["last_index"] = last_index
            page += 1
            time.sleep(1)  # Be polite and avoid hitting the API too quickly. Thank you FEC :)
        else:
            has_more = False

    return all_records

if __name__ == "__main__":
    print(f"Fetching campaign finance data for the {CYCLE} election cycle...")

    # Create a directory to store the data if it doesn't exist
    os.makedirs("raw_senate_data", exist_ok=True)

    for state in TARGET_RACES:
        print(f"Fetching data for state: {state}")
        records = fetch_state_spending(state)

      
        if records:
            df = pd.DataFrame(records)

            # We don't need everything, so let's just save the data I want to keep. You can change this as needed.
            columns_to_keep = [
                "committee_id", "committee_name", "recipient_name", 
                "disbursement_date", "disbursement_amount", 
                "disbursement_description", "disbursement_purpose_category",
                "recipient_city", "recipient_state"
            ]

            # Keep only the columns we care about and actually exist in the DataFrame
            df_filtered = df[[col for col in columns_to_keep if col in df.columns]]

            # Track the number of records we have for each state.
            df_filtered["target_state"] = state

            # Writing out state files.
            output_path = f"raw_senate_data/senate_spending_{state}.csv"
            df_filtered.to_csv(output_path, index=False)
            print(f"Filtered data for state {state} saved to {output_path}")
        else:
            print(f"No data found for state {state}")

        print(f"Finished processing state: {state}\n")
        
    print("\n Pipeline complete. All data fetched and saved successfully.")
