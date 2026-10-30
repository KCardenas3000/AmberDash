import os
import pandas as pd
import sqlite3

def build_database():
    # Get the directory where db_ingest.py lives, then find the project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    # Set paths pointing to the data folder and project root
    csv_path = os.path.join(project_root, "data", "final_battleground_senate_audit.csv")
    db_path = os.path.join(project_root, "data", "amberdash.db")
    
    print(f"Looking for CSV at: {csv_path}")
    
    if not os.path.exists(csv_path):
        print(f"Error: Could not find '{csv_path}'. Check your file name in the data/ folder.")
        return

    conn = sqlite3.connect(db_path)
    print(f"Connected to SQLite database at: {db_path}")
    
    # 1. Load merged CSV records from data directory
    df_disbursements = pd.read_csv(csv_path)
    
    # 2. Store raw disbursements into SQLite table
    df_disbursements.to_sql("raw_disbursements", conn, if_exists="replace", index=False)
    print(f"Stored {len(df_disbursements)} records into table 'raw_disbursements'.")
    
    # 3. Create a distinct Committee reference table
    if "committee_id" in df_disbursements.columns:
        df_committees = df_disbursements[["committee_id", "committee_party", "target_state"]].drop_duplicates()
        df_committees.to_sql("dim_committees", conn, if_exists="replace", index=False)
        print(f"Stored {len(df_committees)} unique committees into table 'dim_committees'.")
        
    conn.close()
    print("Database build complete! Saved to data/amberdash.db")

if __name__ == "__main__":
    build_database()