import os
import pandas as pd

input_candidates = [
    "data/final_battleground_senate_audit.csv",
    "final_battleground_senate_audit.csv",
    "data/powerbi_ready_senate_audit.csv",
]

input_path = next((path for path in input_candidates if os.path.exists(path)), None)
if input_path is None:
    raise FileNotFoundError(
        "No input CSV found. Expected one of: "
        "data/final_battleground_senate_audit.csv, "
        "final_battleground_senate_audit.csv, "
        "data/powerbi_ready_senate_audit.csv"
    )

df = pd.read_csv(input_path)

def categorize_spending(desc):
    if pd.isna(desc):
        return "Uncategorized / Other"
    desc_upper = str(desc).upper()
    if any(k in desc_upper for k in ["MEDIA", "AD", "DIGITAL", "TV", "RADIO", "PRINT"]):
        return "Media & Advertising"
    elif any(k in desc_upper for k in ["PAYROLL", "SALARY", "STAFF", "COMPENSATION"]):
        return "Staff & Payroll"
    elif any(k in desc_upper for k in ["CONSULTING", "STRATEGY", "ADVISORY"]):
        return "Consulting & Strategy"
    elif any(k in desc_upper for k in ["MAIL", "POSTAGE", "PRINTING"]):
        return "Direct Mail & Print"
    elif any(k in desc_upper for k in ["TRAVEL", "FLIGHT", "HOTEL", "LODGING"]):
        return "Travel & Operations"
    elif any(k in desc_upper for k in ["FUNDRAISING", "DONOR", "EVENT"]):
        return "Fundraising Events"
    else:
        return "Operational & Miscellaneous"

df["spending_category_clean"] = df["disbursement_description"].apply(categorize_spending)
output_path = "data/powerbi_ready_senate_audit.csv"
df.to_csv(output_path, index=False)
print(f"Updated CSV saved as {output_path}!")