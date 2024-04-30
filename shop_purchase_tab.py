import streamlit as st
from data_management import load_data, load_employee_names

def shop_purchase_tab():
    st.title("Shop Purchase Account")

    # Check if the CSV file exists
    try:
        data, last_closing_cash  = load_data()
        employee_names = load_employee_names()
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
    expected_columns = ["Date", "Employee 1", "Employee 2", "Employee 3", "Employee 4", "Cleaning", "Other Expenses Name", "Other Expenses Amount", "Other Expenses Name_1", "Other Expenses Amount_1", "Expenses Shop"]
    
    # If the columns are not all present, display an error message
    if not all(col in data.columns for col in expected_columns):
        st.error("The data structure has changed or some columns are missing. Please check the CSV file.")
    else:
        # Display the data with the specified columns
        st.write(data[expected_columns])   
