

import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

#st.set_page_config(page_title="Page Title", layout="wide")
st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)




# Title of the app
#st.title("Upload Customer Data")

# File uploader
uploaded_file = st.file_uploader("Upload a file", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Read the file into a dataframe
    if uploaded_file.name.endswith("csv"):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith("xlsx"):
        df = pd.read_excel(uploaded_file)

    st.session_state["sd"]=df

    # Display file contents with AG Grid
    st.subheader("File Contents")

    # Configuring AG Grid options
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=True)  # Optional: Add pagination
    gb.configure_side_bar()  # Optional: Enable side bar filters
    gb.configure_default_column(editable=True)  # Optional: Allow editing
    grid_options = gb.build()

    # Display AG Grid with options
    AgGrid(df, gridOptions=grid_options)
else:
    st.write("Please upload a CSV or Excel file to view its contents.")
