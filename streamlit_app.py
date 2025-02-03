import streamlit as st
import pandas as pd

def process_file(uploaded_file):
    # Load the Excel file
    xls = pd.ExcelFile(uploaded_file)
    df = xls.parse(xls.sheet_names[0])  # Assuming first sheet is relevant
    
    # Create a dictionary mapping spaces to organisations
    spaces_dict = {}
    for _, row in df.iterrows():
        organisation = row['Organisation']
        spaces = str(row['Spaces']).split(',') if pd.notna(row['Spaces']) else []
        
        for space in spaces:
            space = space.strip()
            if space:
                if space in spaces_dict:
                    spaces_dict[space].append(organisation)
                else:
                    spaces_dict[space] = [organisation]
    
    return spaces_dict

# Streamlit UI
st.title("Spaces to Organisations Mapping")

uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

if uploaded_file is not None:
    spaces_dict = process_file(uploaded_file)
    st.write("### Spaces Dictionary:")
    st.json(spaces_dict)
