import streamlit as st
from data_management import load_data, load_employee_names
import pandas as pd
import os

import datetime
from datetime import date, datetime, timedelta
from data_management import csv_file, employee_csv, employee_salary_Advance_bankTransfer_csv,employee_salary_data_csv
from ui_helpers import display_data

        
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

def load_salary_data():
    try:
        return pd.read_csv(employee_salary_data_csv, parse_dates=['Month'], dayfirst=False)
    except FileNotFoundError:
        st.error("Salary data file is missing. Please ensure it exists in the correct location.")
        return None

def update_sales_data():
    salary_data = load_salary_data()
    if salary_data is None:
        return  # Exit if the data couldn't be loaded
    
    # Ensure 'Month' is in datetime format; parse again if necessary
    if not pd.api.types.is_datetime64_any_dtype(salary_data['Month']):
        salary_data['Month'] = pd.to_datetime(salary_data['Month'], errors='coerce')
        if salary_data['Month'].isnull().any():
            st.error("There are invalid date entries in the 'Month' column.")
            return

    salary_data = salary_data.sort_values(by='Month', ascending=False)

    st.write("### Update Total Sales Data")

    # User selects the month and employee
    months = salary_data['Month'].dt.strftime('%Y-%m').unique()
    selected_month = st.selectbox("Select Month", options=months)
    selected_employee = st.selectbox("Select Employee", options=salary_data['Employee'].unique())

    # Filter data for selected month and employee
    filtered_data = salary_data[(salary_data['Month'].dt.strftime('%Y-%m') == selected_month) & 
                                (salary_data['Employee'] == selected_employee)]

    if not filtered_data.empty:
        current_sales = filtered_data.iloc[0]['Total Sales']
        st.write(f"Current Total Sales for {selected_employee} in {selected_month}: {current_sales}")
    else:
        current_sales = 0
        st.write(f"No sales data found for {selected_employee} in {selected_month}. You can add new data.")

    # Allow user to enter new total sales
    new_sales = st.number_input("Enter New Total Sales", value=int(current_sales))

    if st.button("Update Sales"):
        if filtered_data.empty:
            # Add new entry
            new_data = {
                'Month': pd.Period(selected_month, freq='M').start_time,
                'Employee': selected_employee,
                'Bank Transfers': 0,
                'Cash Withdrawn': 0,
                'Total Salary Advance': 0,
                'Total Sales': new_sales,
                'Salary': new_sales / 2,
                'Balance': new_sales / 2,
                'Balance Todate': new_sales / 2  # Adjust according to actual calculation rules
            }
            salary_data = salary_data.append(new_data, ignore_index=True)
        else:
            # Update existing entry
            salary_data.loc[filtered_data.index, 'Total Sales'] = new_sales
            salary_data.loc[filtered_data.index, 'Salary'] = new_sales / 2

        # Save updated data back to CSV
        salary_data.to_csv(employee_salary_data_csv, index=False)
        st.success("Sales data updated successfully.")
        
    display_data(salary_data,"Employee Salary")
  

def employee_salary_tab():
    st.title("Employee Salary Accounts")

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
    
    if os.path.isfile(employee_salary_Advance_bankTransfer_csv):
        employee_salary_Advance_bankTransfer = pd.read_csv(employee_salary_Advance_bankTransfer_csv)
        display_data(employee_salary_Advance_bankTransfer,"Employee Advance Bank Transfer")
    else:
        st.error("File {employee_salary_Advance_bankTransfer_csv} is missing! Please check the CSV file path.")

    expected_columns = ["Date", employee_names_list[0], employee_names_list[1], employee_names_list[2], employee_names_list[3]]
    
    if not all(col in data_copy.columns for col in expected_columns):
        st.error("The data structure has changed or some columns are missing. Please check the CSV file.")
    else:
        employee_cash_withdrawn_data = data_copy[expected_columns]
        display_data(employee_cash_withdrawn_data,"Employee Cash Advance")
        
    update_sales_data()
    
   

