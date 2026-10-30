import pandas as pd

df = pd.read_csv("data/final_battleground_senate_audit.csv")

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
df.to_csv("powerbi_ready_senate_audit.csv", index=False)
print("Updated CSV saved as powerbi_ready_senate_audit.csv!")