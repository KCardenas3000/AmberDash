import os
import sqlite3
import pandas as pd

def run_sql_analytics():
    # Find project root relative to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    db_path = os.path.join(project_root, "data", "amberdash.db")

    if not os.path.exists(db_path):
        print(f"Error: Database file not found at '{db_path}'. Run db_ingest.py first!")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print(f"Executing SQL transformations on '{db_path}'...")

    # 1. Drop existing view if present and re-create it cleanly
    cursor.execute("DROP VIEW IF EXISTS v_state_party_spending;")
    cursor.execute("""
    CREATE VIEW v_state_party_spending AS
    SELECT 
        target_state,
        committee_party,
        COUNT(*) as transaction_count,
        SUM(disbursement_amount) as total_disbursement,
        AVG(disbursement_amount) as avg_disbursement
    FROM raw_disbursements
    WHERE disbursement_amount > 0
    GROUP BY target_state, committee_party;
    """)
    conn.commit()
    print("Successfully created SQL View: 'v_state_party_spending'")
    
    # 2. Query top vendors directly from SQLite
    top_vendors = pd.read_sql_query("""
        SELECT 
            recipient_name,
            SUM(disbursement_amount) as total_spent
        FROM raw_disbursements
        WHERE disbursement_amount > 0
        GROUP BY recipient_name
        ORDER BY total_spent DESC
        LIMIT 10;
    """, conn)
    
    print("\n--- Top 10 Vendors (Queried via SQLite) ---")
    print(top_vendors.to_string(index=False))
    
    conn.close()

if __name__ == "__main__":
    run_sql_analytics()