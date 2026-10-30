import os
import sqlite3
import pandas as pd
import streamlit as st

logo_path = os.path.join("assets", "AD_logo_beta_1.png")

st.set_page_config(page_title="AmberDash", page_icon="🐰", layout="wide", initial_sidebar_state = "expanded")

col_logo, col_title = st.columns([1, 6])

with col_logo:
    if os.path.exists(logo_path):
        st.image(logo_path, width=110)
    else:
        st.title("🐰")

with col_title:
    st.title("Project AmberDash")
    st.caption("Federal Campaign Finance Audit Pipeline | U.S. Senate Battleground Races")

st.markdown("---")

@st.cache_data
def load_data():
    db_path = os.path.join("data", "amberdash.db")
    if not os.path.exists(db_path):
        return pd.DataFrame()
    
    conn = sqlite3.connect(db_path)
    query = """
    SELECT 
        target_state,
        committee_party,
        recipient_name,
        disbursement_amount,
        disbursement_description,
        spending_category_clean
    FROM raw_disbursements
    WHERE disbursement_amount > 0
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

df = load_data()

if df.empty:
    st.warning("No data available. Please ensure the database is populated.")

st.sidebar.header("Audit Filters")
all_parties = sorted(list(df["committee_party"].dropna().unique()))
selected_parties = st.sidebar.multiselect("Party Affiliation", options=all_parties, default=all_parties)

all_states = sorted(list(df["target_state"].dropna().unique()))
selected_states = st.sidebar.multiselect("Target Battleground State", options=all_states, default=all_states)

filtered_df = df[
    (df["committee_party"].isin(selected_parties)) &
    (df["target_state"].isin(selected_states))
]

st.subheader("Key Spending Metrics")
c1, c2, c3, c4 = st.columns(4)

total_spend = filtered_df["disbursement_amount"].sum()
total_txs = len(filtered_df)
avg_spend = filtered_df["disbursement_amount"].mean() if total_txs > 0 else 0
active_states = filtered_df["target_state"].nunique()

c1.metric("Total Tracked Spending", f"${total_spend:,.2f}")
c2.metric("Total Transactions", f"{total_txs:,}")
c3.metric("Average Transaction", f"${avg_spend:,.2f}")
c4.metric("Active States Selected", f"{active_states}")

st.markdown("---")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Top Expenditure Categories")
    cat_summary = (
        filtered_df.groupby("spending_category_clean")["disbursement_amount"]
        .sum()
        .reset_index()
        .sort_values(by="disbursement_amount", ascending=False)
    )
    st.bar_chart(data=cat_summary, x="spending_category_clean", y="disbursement_amount", height=320)

with chart_col2:
    st.subheader("Total Spending by Target State")
    state_summary = (
        filtered_df.groupby("target_state")["disbursement_amount"]
        .sum()
        .reset_index()
        .sort_values(by="disbursement_amount", ascending=False)
    )
    st.bar_chart(data=state_summary, x="target_state", y="disbursement_amount", height=320)

st.markdown("---")

st.subheader("Transaction Audit Inspector")

search = st.text_input("Search Recipient or Description", "")
if search:
    filtered_df = filtered_df[
        filtered_df["recipient_name"].str.contains(search, case=False, na=False) |
        filtered_df["disbursement_description"].str.contains(search, case=False, na=False)
    ]

st.dataframe(
    filtered_df[["target_state", "committee_party", "recipient_name", "disbursement_amount", "spending_category_clean", "disbursement_description"]],
    use_container_width=True,
    height=380
)

st.caption("Project AmberDash Phase 1 MVP — OpenFEC API Ingestion & SQLite Engine 🐰")