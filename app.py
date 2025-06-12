import streamlit as st
import pandas as pd

st.title("CSV Uploader and Viewer")
st.markdown("Upload a CSV file to view its contents in an expandable table.")
st.markdown("If you encounter errors after uploading, your CSV might have an unsupported encoding. The application will attempt to read common encodings (UTF-8, ISO-8859-1, CP1252). If issues persist, try saving your CSV file as UTF-8 and re-uploading.")
st.markdown("---") # Adds a horizontal rule for separation

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = None
    error_message = None
    tried_encodings = []

    # Try UTF-8 first
    try:
        uploaded_file.seek(0) # Reset file pointer to the beginning
        df = pd.read_csv(uploaded_file, encoding='utf-8')
        tried_encodings.append('utf-8')
    except UnicodeDecodeError:
        # Try ISO-8859-1 if UTF-8 fails
        try:
            uploaded_file.seek(0) # Reset file pointer
            df = pd.read_csv(uploaded_file, encoding='iso-8859-1')
            tried_encodings.append('iso-8859-1')
        except UnicodeDecodeError:
            # Try cp1252 if ISO-8859-1 also fails
            try:
                uploaded_file.seek(0) # Reset file pointer
                df = pd.read_csv(uploaded_file, encoding='cp1252')
                tried_encodings.append('cp1252')
            except UnicodeDecodeError:
                error_message = "Error: Could not decode the file with UTF-8, ISO-8859-1, or CP1252 encoding. Please check the file encoding."
                tried_encodings.extend(['cp1252']) # cp1252 was the last one tried
            except pd.errors.ParserError:
                error_message = "Error: Could not parse the CSV file. Please ensure it is a valid CSV, even after trying other encodings."
            except Exception as e:
                error_message = f"An unexpected error occurred while trying alternative encodings: {e}"
        except pd.errors.ParserError:
            error_message = "Error: Could not parse the CSV file. Please ensure it is a valid CSV, even after trying other encodings."
        except Exception as e:
            error_message = f"An unexpected error occurred while trying alternative encodings: {e}"
    except pd.errors.ParserError:
        error_message = "Error: Could not parse the CSV file with UTF-8 encoding. Please ensure it is a valid CSV."
    except Exception as e:
        error_message = f"An unexpected error occurred with UTF-8 encoding: {e}"

    if df is not None:
        with st.expander("View Uploaded Data"):
            st.dataframe(df)
        # Optionally, inform the user which encoding worked, if it wasn't the first one.
        # if tried_encodings and tried_encodings[-1] != 'utf-8' and len(tried_encodings) > 1:
        #    st.info(f"File successfully read using {tried_encodings[-1]} encoding.")
    elif error_message:
        st.error(error_message)
