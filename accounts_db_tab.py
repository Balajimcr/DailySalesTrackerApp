import streamlit as st
from data_management import load_data
import pandas as pd  # Make sure pandas is imported

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

    def highlight_difference(val):
        """
        Highlights the 'Cash Difference' cell based on its value.
        """
        color = 'red' if val > 100 else ('green' if val < 100 else 'none')
        return f'background-color: {color}'

    # Applying the style to the dataframe
    styled_data = data.style.applymap(highlight_difference, subset=['Cash Difference'])
    st.dataframe(styled_data)  # Display the styled dataframe

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
    
    # Format the 'Date' column
    if 'Date' in data.columns:
        data['Date'] = pd.to_datetime(data['Date']).dt.strftime('%Y-%m-%d (%A)')
        # Sort the DataFrame by index in descending order
        data = data.sort_values(by='Date', ascending=False)
        
    # Ensure the expected columns are present
    important_columns = ["Date", "Total Sales POS", "Cash Difference", "Closing Cash"]
    
    # Ensure the expected columns are present
    expected_columns = ["Date", "Opening Cash", "Total Sales POS", "Paytm", "Denomination Total", "Cash Withdrawn", "Total Cash", "Closing Cash", "Cash Difference"]
    
    # If the columns are not all present, display an error message
    if not all(col in data.columns for col in expected_columns):
        st.error("The data structure has changed or some columns are missing. Please check the CSV file.")
    else:
        # Display the data with the specified columns
        display_data(data[important_columns])
        
        display_data(data[expected_columns])
