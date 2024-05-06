import streamlit as st
from data_management import load_data, load_employee_names
import pandas as pd
import os
import datetime
from datetime import date, datetime, timedelta
from data_management import csv_file, employee_csv, employee_salary_Advance_bankTransfer_csv


def custom_table_style():
    # CSS to inject contained in a triple-quoted string
    table_style = """
    <style>
    /* Adds styling to the table headers */
    thead tr th {
        background-color: #f0f0f0;  /* Light grey background */
        color: black;               /* Black text */
        font-size: 22pt;           /* Larger font size */
    }
    /* Style for the table data cells */
    tbody tr td {
        color: black;               /* Black text */
        font-size: 20pt;           /* Slightly smaller font size than headers */
    }
    </style>
    """

    # Display the CSS style
    st.markdown(table_style, unsafe_allow_html=True)

def display_data(data):
    custom_table_style()  # Call the style function
    
    styled_data = data
    st.dataframe(styled_data)  # Display the styled dataframe
    
def save_data_to_csv(new_data, file_name=employee_salary_Advance_bankTransfer_csv):
    # Check if file exists
    if not os.path.isfile(file_name):
        # Create a new DataFrame and save it
        pd.DataFrame([new_data]).to_csv(file_name, index=False)
    else:
        # Load existing data and append new data
        existing_data = pd.read_csv(file_name)
        new_frame = pd.DataFrame([new_data])
        updated_data = pd.concat([existing_data, new_frame], ignore_index=True)
        updated_data.to_csv(file_name, index=False)
    return pd.read_csv(file_name)  # Return updated data

def employee_salary_tab():
    st.title("Employee Salary Account")

    # Check if the CSV file exists
    try:
        data, last_closing_cash = load_data()
        employee_names_list = load_employee_names()  # Load employee names as a list
    except FileNotFoundError:
        st.error("The database file is missing. Please ensure it exists in the correct location.")
        return
    except pd.errors.ParserError:
        st.error("Error parsing the CSV file. Please check the file format.")
        return
    
    # Create a copy of the data for modification
    data_copy = data.copy()

    # Assuming employee_names_list is correctly ordered to replace "Employee 1", "Employee 2", etc.
    # Create a dictionary mapping old column names to new names based on the loaded list
    column_name_mapping = {
        "Employee 1": employee_names_list[0],
        "Employee 2": employee_names_list[1],
        "Employee 3": employee_names_list[2],
        "Employee 4": employee_names_list[3]
    }

    # Rename columns in the copy of the DataFrame
    data_copy.rename(columns=column_name_mapping, inplace=True)

    if data_copy.empty:
        st.warning("No data found. The database might be empty or filtered out.")
        return

    if 'Date' in data_copy.columns:
        data_copy['Date'] = pd.to_datetime(data_copy['Date']).dt.strftime('%Y-%m-%d (%A)')
        data_copy = data_copy.sort_values(by='Date', ascending=False)
        
    # User Inputs
    input_date = st.date_input("Date", value=date.today(), format="DD-MM-YYYY")
    input_amount = st.number_input("Amount", min_value=0, step=1000) 
    input_employee = st.selectbox("Employee", options=employee_names_list)
    input_comments = st.text_input("Comments")

    if st.button("Save Entry"):
        new_entry = {
            "Date": input_date.strftime('%d-%m-%Y'),
            "Amount": input_amount,
            "Employee": input_employee,
            "Comments": input_comments
        }
        save_data_to_csv(new_entry)

    # Display existing data
    st.markdown(
            f'<div style="color: black; font-size: 24px; font-weight: bold;">Employee Salary Advance Bank Transfers:</div>',
            unsafe_allow_html=True
        )
    
    if os.path.isfile(employee_salary_Advance_bankTransfer_csv):
        employee_salary_Advance_bankTransfer = pd.read_csv(employee_salary_Advance_bankTransfer_csv)
        display_data(employee_salary_Advance_bankTransfer)

    expected_columns = ["Date", employee_names_list[0], employee_names_list[1], employee_names_list[2], employee_names_list[3]]
    
    if not all(col in data_copy.columns for col in expected_columns):
        st.error("The data structure has changed or some columns are missing. Please check the CSV file.")
    else:
        display_data(data_copy[expected_columns])
    
   

