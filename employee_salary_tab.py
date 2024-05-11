import streamlit as st
from data_management import load_data, load_employee_names
import pandas as pd
import os

import datetime
from datetime import date, datetime, timedelta
from ui_helpers import displayhtml_data
from data_management import csv_file, employee_csv, employee_salary_Advance_bankTransfer_csv,employee_salary_data_csv


def display_data(dataframe, title):
    """Display a dataframe with a title."""
    st.markdown(f'<div style="color: black; font-size: 24px; font-weight: bold;">{title}:</div>', unsafe_allow_html=True)
    st.dataframe(dataframe)
        
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
        updated_data.to_csv(file_name, index=False,encoding="utf-8")
    return pd.read_csv(file_name)  # Return updated data

def load_salary_data():
    try:
        return pd.read_csv(employee_salary_data_csv, parse_dates=['Month'], dayfirst=False)
    except FileNotFoundError:
        st.error("Salary data file is missing. Please ensure it exists in the correct location.")
        return None
    
def aggregate_financials(bank_transfer_df, cash_withdrawn_df):
    """
    Aggregate financial data month-wise for bank transfers and cash withdrawals.

    Args:
    - bank_transfer_df (DataFrame): Data containing bank transfer details.
    - cash_withdrawn_df (DataFrame): Data containing cash withdrawn details.

    Returns:
    - DataFrame: Aggregated financial data per month and employee.
    """
    # Convert date strings to datetime objects for easier manipulation
    bank_transfer_df['Date'] = pd.to_datetime(bank_transfer_df['Date'], dayfirst=True)
    cash_withdrawn_df['Date'] = pd.to_datetime(cash_withdrawn_df['Date'], dayfirst=True)

    # Group and resample bank transfer data by month
    monthly_bank_transfers = bank_transfer_df.groupby(['Employee', pd.Grouper(key='Date', freq='M')]).sum().reset_index()
    monthly_bank_transfers['Month'] = monthly_bank_transfers['Date'].dt.strftime('%b-%Y')
    monthly_bank_transfers.rename(columns={'Amount': 'Monthly Bank Transfers', 'Employee': 'Employee Name'}, inplace=True)
    monthly_bank_transfers.drop(columns=['Date'])
    monthly_bank_transfers = monthly_bank_transfers.reindex(columns=["Month", "Employee Name",'Monthly Bank Transfers'])

    # Melt cash_withdrawn_df to make it long format, preparing it for grouping
    melted_cash_withdrawn = pd.melt(cash_withdrawn_df, id_vars=['Date'], var_name='Employee Name', value_name='Amount')
    melted_cash_withdrawn['Month'] = melted_cash_withdrawn['Date'].dt.to_period('M')
    
    # Aggregate the melted data by month and employee for the 'Amount' column only
    monthly_cash_withdrawn = melted_cash_withdrawn.groupby(['Month', 'Employee Name']).agg({'Amount': 'sum'}).reset_index()
    monthly_cash_withdrawn['Month'] = monthly_cash_withdrawn['Month'].dt.strftime('%b-%Y')
    monthly_cash_withdrawn.rename(columns={'Amount': 'Monthly Cash Withdrawn'}, inplace=True)

    # Merge the DataFrames on 'Month' and 'Employee Name'
    financial_summary = pd.merge(monthly_cash_withdrawn, monthly_bank_transfers, on=['Month', 'Employee Name'], how='left')

    # Fill NaN values with 0 for the Monthly Bank Transfers column
    financial_summary['Monthly Bank Transfers'].fillna(0, inplace=True)
    
    #display_data(monthly_bank_transfers,"Monthly Bank Transfers")
    #display_data(monthly_cash_withdrawn,"Monthly Cash Withdrawn")
    display_data(financial_summary,"Monthly Financial Summary")

    return financial_summary

def update_sales_data():
    salary_data = load_salary_data()
    if salary_data is None:
        return  # Exit if the data couldn't be loaded
    
    st.write("### Update Total Sales Data")

    # Format 'Month' for display and use in selection
    months = salary_data['Month'].dt.strftime('%b-%Y').unique()
    selected_month = st.selectbox("Select Month", options=months)

    # Convert selected month back to datetime for comparison
    selected_month_datetime = pd.to_datetime(selected_month, format='%b-%Y')

    # Create a dataframe to collect updated sales data
    updates = []

    for employee in salary_data['Employee Name'].unique():
        # Filter data for the selected month and employee
        filtered_data = salary_data[(salary_data['Month'].dt.strftime('%b-%Y') == selected_month) & 
                                    (salary_data['Employee Name'] == employee)]
        
        if not filtered_data.empty:
            current_sales = filtered_data.iloc[0]['Total Sales']
        else:
            current_sales = 0

        # Use Streamlit columns to display employee name, current sales, and input for new sales
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"{employee}")
        with col2:
            st.write(f"{current_sales}")
        with col3:
            new_sales = st.number_input(f"New Sales", key=employee, value=int(current_sales))
        
        # Collect data for updates
        updates.append((employee, new_sales, filtered_data.index))

    if st.button("Update Sales"):
        for employee, new_sales, idx in updates:
            if idx.empty:
                # Add new entry
                new_data = {
                    'Month': selected_month_datetime,  # Use the datetime format for consistency
                    'Employee Name': employee,
                    'Monthly Bank Transfers': 0,
                    'Monthly Cash Withdrawn': 0,
                    'Total Salary Advance': 0,
                    'Total Sales': new_sales,
                    'Salary': new_sales / 2,
                    'Balance': 0,
                    'Balance Till date': 0
                }
                salary_data = salary_data.append(new_data, ignore_index=True)
            else:
                # Update existing entries
                salary_data.loc[idx, 'Total Sales'] = new_sales
                salary_data.loc[idx, 'Salary'] = new_sales / 2

        # Save the updated data back to the CSV
        salary_data.to_csv(employee_salary_data_csv, index=False,encoding="utf-8")
        st.success("Sales data updated successfully.")
        
    # Format date for display when necessary
    salary_data['Month'] = salary_data['Month'].dt.strftime('%b-%Y')
    
    display_data(salary_data, "Employee Salary")
    
    return salary_data
  

def calculate_financials(month, employee, adv_bank_transfer_df, cash_withdrawn_df, previous_balances):
    """Compute financial details for each employee for a given month."""
    salary_data = load_salary_data()
    
    # Filter data for the specific month and employee
    bank_transfers = adv_bank_transfer_df[(adv_bank_transfer_df['Date'] == month) & 
                                          (adv_bank_transfer_df['Employee'] == employee)]
    cash_withdrawals = cash_withdrawn_df[(cash_withdrawn_df['Date'] == month) & 
                                         (cash_withdrawn_df['Employee'] == employee)]

    # Sum total advances and withdrawals
    total_bank_transfers = bank_transfers['Amount'].sum()
    total_cash_withdrawn = cash_withdrawals['Amount'].sum()

    # Total advances
    total_advances = total_bank_transfers + total_cash_withdrawn
    
    # Fetch sales data
    # Assuming sales data includes a column 'Total Sales' for each employee per month
    sales_info = salary_data[(salary_data['Month'] == month) & (salary_data['Employee'] == employee)]
    total_sales = sales_info['Total Sales'].sum() if not sales_info.empty else 0

    # Salary calculations based on sales
    salary = total_sales / 2  # Assuming salary is half of the sales

    # Fetch previous balance; if not available, initialize to 0
    prev_month_key = (datetime.strptime(month, '%b-%Y') - pd.DateOffset(months=1)).strftime('%b-%Y')
    prev_balance_key = f"{prev_month_key}-{employee}"
    previous_balance = previous_balances.get(prev_balance_key, 0)

    # Compute current balance and update for this month
    balance_curr = total_advances - salary
    balance_till_date = previous_balance + balance_curr

    # Store the current balance till date for future use
    current_month_key = f"{month}-{employee}"
    previous_balances[current_month_key] = balance_till_date

    return {
        "Total Bank Transfers": total_bank_transfers,
        "Total Cash Withdrawn": total_cash_withdrawn,
        "Total Sales": total_sales,
        "Salary": salary,
        "Balance Current": balance_curr,
        "Balance Till Date": balance_till_date
    }


def update_financials_over_time(start_month, end_month, employees, adv_bank_transfer_df, cash_withdrawn_df):
    """Update financial records over a range of months."""
    month_range = pd.date_range(start=start_month, end=end_month, freq='MS').strftime('%b-%Y')
    results = []
    
    # Dictionary to store balance till date for each month and employee
    previous_balances = {}

    for month in month_range:
        for employee in employees:
            results.append({
                "Month": month,
                "Employee": employee,
                **calculate_financials(month, employee, adv_bank_transfer_df, cash_withdrawn_df,previous_balances)
            })

    return pd.DataFrame(results)


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
    employee_sa_cash_withdrawn = data.copy()

    # Assuming employee_names_list is correctly ordered to replace "Employee 1", "Employee 2", etc.
    # Create a dictionary mapping old column names to new names based on the loaded list
    column_name_mapping = {
        "Employee 1": employee_names_list[0],
        "Employee 2": employee_names_list[1],
        "Employee 3": employee_names_list[2],
        "Employee 4": employee_names_list[3]
    }

    # Rename columns in the copy of the DataFrame
    employee_sa_cash_withdrawn.rename(columns=column_name_mapping, inplace=True)

    if employee_sa_cash_withdrawn.empty:
        st.warning("No data found. The database might be empty or filtered out.")
        return

    if 'Date' in employee_sa_cash_withdrawn.columns:
        employee_sa_cash_withdrawn['Date'] = pd.to_datetime(employee_sa_cash_withdrawn['Date']).dt.strftime('%d-%m-%Y')
        employee_sa_cash_withdrawn = employee_sa_cash_withdrawn.sort_values(by='Date', ascending=False)
        
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
    
    employee_cash_withdrawn_data =[]
    
    if not all(col in employee_sa_cash_withdrawn.columns for col in expected_columns):
        st.error("The data structure has changed or some columns are missing. Please check the CSV file.")
    else:
        employee_cash_withdrawn_data = employee_sa_cash_withdrawn[expected_columns]
        display_data(employee_cash_withdrawn_data,"Employee Cash Advance")
        
    employee_Salary_data = update_sales_data()
    
    # Sort by Employee and then by Month
    employee_Salary_data.sort_values(by=['Employee Name', 'Month'], inplace=True)
    
    start_month = 'Mar-2024'
    end_month   = datetime.now().strftime('%b-%Y')

    adv_bank_transfer_df = pd.read_csv(employee_salary_Advance_bankTransfer_csv)
    cash_withdrawn_df = employee_cash_withdrawn_data

    # Assuming you have a way to fetch or define a list of employees
    employees = load_employee_names()  # Load names or define list
    
    financial_summary = aggregate_financials(adv_bank_transfer_df, cash_withdrawn_df)
    
     # Merge the DataFrames on 'Month' and 'Employee Name'
    financial_summary = pd.merge(financial_summary, employee_Salary_data, on=['Month', 'Employee Name'], how='left')
    
