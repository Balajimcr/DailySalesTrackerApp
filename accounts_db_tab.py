import streamlit as st
from data_management import load_data

def accounts_db_tab():
    st.title("Daily Accounts Database")

    # Check if the CSV file exists
    try:
        data, last_closing_cash = load_data()
    except FileNotFoundError:
        st.error("The database file is missing. Please ensure it exists in the correct location.")
        return
    except pd.errors.ParserError:
        st.error("Error parsing the CSV file. Please check the file format.")
        return

    
    # Check if the DataFrame is empty
    if data.empty:
        st.warning("No data found. The database might be empty or filtered out.")
        return
    
    # Ensure the expected columns are present
    expected_columns = ["Date", "Opening Cash", "Total Sales POS", "Paytm", "Denomination Total", "Cash Withdrawn", "Total Cash", "Closing Cash", "Cash Difference"]
    
    # If the columns are not all present, display an error message
    if not all(col in data.columns for col in expected_columns):
        st.error("The data structure has changed or some columns are missing. Please check the CSV file.")
    else:
        # Display the data with the specified columns
        st.write(data[expected_columns])
