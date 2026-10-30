import glob
import pandas as pd

# We're going to need to find all the CSV files in the raw_senate_data directory and merge them into a single DataFrame. This will make it easier to analyze the data later on.
all_csv_files = glob.glob("raw_senate_data/*.csv")

print(f"Found {len(all_csv_files)} state CSV files to merge.")

# Read and stack all the CSV files into a single DataFrame
master_df = pd.concat((pd.read_csv(f) for f in all_csv_files), ignore_index=True)

# Something I want to try out is name standardization. The FEC API has a lot of different ways to represent candidate names, so I'm going to try to standardize them to make it easier to analyze the data later on.
# For example, "JFacebook" and "Facebook Inc." are the same entity, but they are represented differently in the FEC data. I'm going to try to standardize them to "Facebook" to make it easier to analyze the data later on.
# This is a very basic example, but it should give you an idea of how to approach this problem. You can expand on this as needed....

master_df['recipient_clean'] = (
    master_df['recipient_name']
    .str.upper()
    .str.strip()
        .str.replace(r"\s+(LLC|INC|CORP|LTD|GROUP)\.?$", "", regex=True)
)

# Save the merged DataFrame to a new CSV file for later analysis
output_file = "merged_battleground_senate_data.csv"
master_df.to_csv(output_file, index=False)

print(f"It works! Merged data saved to {output_file}. Total records: {len(master_df)}")
print(f"File saved to: {output_file}")
