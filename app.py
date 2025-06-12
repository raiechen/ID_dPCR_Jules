import streamlit as st
import pandas as pd

st.title("CSV Uploader and Viewer")
st.markdown("Upload a CSV file to view its contents in an expandable table.")
st.markdown("---") # Adds a horizontal rule for separation

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    try:
        # Can be used to read CSV files ankoor IO object.
        df = pd.read_csv(uploaded_file)
        with st.expander("View Uploaded Data"):
            st.dataframe(df)
    except pd.errors.ParserError:
        st.error("Error: Could not parse the CSV file. Please ensure it is a valid CSV.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
