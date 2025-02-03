import streamlit as st
import pandas as pd
import re
import matplotlib.pyplot as plt

def clean_space_id(space_id):
    if pd.isna(space_id):
        return None
    cleaned = re.sub(r'\D', '', str(space_id))  # Remove non-numeric characters
    return int(cleaned) if cleaned else None

def process_files(excel_file, csv_file):
    # Load Excel file
    xls = pd.ExcelFile(excel_file)
    df = xls.parse(xls.sheet_names[0])  # Assuming first sheet is relevant
    df['Spaces'] = df['Spaces'].apply(clean_space_id)
    df_clean = df.dropna(subset=['Spaces'])
    
    # Load CSV file
    df_csv = pd.read_csv(csv_file)
    df_csv['metadata.activity_partition_id'] = df_csv['metadata.activity_partition_id'].apply(clean_space_id)
    
    # Create a mapping from Spaces to Organisations
    spaces_to_org = {row['Spaces']: row['Organisation'] for _, row in df_clean.iterrows()}
    
    # Map activity IDs to organisations
    df_csv['Organisation'] = df_csv['metadata.activity_partition_id'].map(spaces_to_org)
    
    # Count occurrences per organisation
    org_activity_counts = df_csv['Organisation'].value_counts()
    
    # Get the top 20 most active organisations
    top_20_orgs = org_activity_counts.head(20)
    
    # Identify organisations with no activity in the CSV file
    orgs_with_no_activity = set(df['Organisation']) - set(df_csv['Organisation'].dropna())
    df_orgs_no_activity = pd.DataFrame({'Organisation': list(orgs_with_no_activity)})
    
    return top_20_orgs, df_orgs_no_activity

# Streamlit UI
st.title("Spaces to Organisations Analysis")

excel_file = st.file_uploader("Upload an Excel file", type=["xlsx"])
csv_file = st.file_uploader("Upload a CSV file", type=["csv"])

if excel_file is not None and csv_file is not None:
    top_20_orgs, df_orgs_no_activity = process_files(excel_file, csv_file)
    
    # Display horizontal bar chart of top 20 most active organisations
    st.write("### Top 20 Most Active Organisations")
    fig, ax = plt.subplots(figsize=(12, 6))
    top_20_orgs.sort_values().plot(kind='barh', ax=ax)
    ax.set_xlabel("Activity Count")
    ax.set_ylabel("Organisation")
    ax.set_title("Top 20 Most Active Organisations")
    st.pyplot(fig)
    
    # Show table of organisations with no activity
    st.write("### Organisations with No Referenced Activity")
    st.dataframe(df_orgs_no_activity)
