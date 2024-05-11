import streamlit as st
import pandas as pd
import hashlib
from data_management import load_data, save_data  # Assuming save_data is a function you will define to save data back to CSV

def display_data(data):
    def highlight_difference(val):
        color = 'red' if val > 100 else ('green' if val < 100 else 'none')
        return f'background-color: {color}; color: black;'

    styled_data = data.style.applymap(highlight_difference, subset=['Cash Difference'])
    html = styled_data.to_html(escape=False)
    st.write(html, unsafe_allow_html=True)

def delete_row(data, index):
    """ Removes a row from the dataframe based on the given index. """
    if index in data.index:
        return data.drop(index)
    else:
        st.error("Row index not found in the database.")
        return data
    
def accounts_db_tab():
    st.title("Daily Accounts Database")

    try:
        data, last_closing_cash = load_data()
    except FileNotFoundError:
        st.error("The database file is missing. Please ensure it exists in the correct location.")
        return
    except pd.errors.ParserError:
        st.error("Error parsing the CSV file. Please check the file format.")
        return

    if not data.empty:
        if 'Date' in data.columns:
            data['Date'] = pd.to_datetime(data['Date'])
            data = data.sort_values(by='Date', ascending=False)  # Sort by date in ascending order
            data['Date'] = data['Date'].dt.strftime('%d-%m-%Y')  # Format the date for display after sorting

        expected_columns = ["Date", "Opening Cash", "Closing Cash", "Cash Difference", "Total Sales POS", "Paytm", "Total Cash", "Denomination Total", "Cash Withdrawn"]
        
        if not all(col in data.columns for col in expected_columns):
            st.error("The data structure has changed or some columns are missing.")
            return

        # Layout for row selection, password input, and delete button
        col1, col2, col3 = st.columns(3)
        
        with col1:
            row_to_delete = st.selectbox("Select Row to Delete", options=data.index)
        with col2:
            password = st.text_input("Enter password to delete entry", type="password")
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
        with col3:
            delete_button_clicked = st.button("Delete Row")
        
        if delete_button_clicked and hashed_password == "f20732a590b9312ee8282a5962cc5b90e4c1bbb31e5c537d51857c5a3fab5a41":  # Replace 'password' with the actual password
            data = delete_row(data, row_to_delete)
            data.sort_index(inplace=True)  # Sort back by original index before saving
            save_data(data)  # Save the restored order data back to CSV
            st.success(f"Row {row_to_delete} deleted successfully.")
            
        elif delete_button_clicked:
            st.error("Incorrect password.")

        display_data(data[expected_columns])
    else:
        st.warning("No data found. The database might be empty or filtered out.")
