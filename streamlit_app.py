import streamlit as st
import pandas as pd
from datetime import date


# File path for the CSV file
csv_file = "database_collection.csv"

# Load existing data from the CSV file (if it exists)
try:
    data = pd.read_csv(csv_file)
    # If data exists, get the previous day's closing cash
    last_closing_cash = data["Closing Cash"].iloc[-1]
except (FileNotFoundError, IndexError):
    data = pd.DataFrame(
        columns=[
            "Date",
            "Opening Cash",
            "Expenses Shop",
            "Denomination Total",
            "Total Sales POS",
            "Paytm",
            "Cash Withdrawn",
            "Employee 1",
            "Employee 2",
            "Employee 3",
            "Employee 4",
            "Cleaning",
            "Other Expenses Name",
            "Other Expenses Amount",
            "500",
            "200",
            "100",
            "50",
            "20",
            "10",
            "5",
            "Closing Cash",
        ]
    )
    # If no data, default the opening cash to zero
    last_closing_cash = 0

st.title("Daily Accounts")

# Create a two-column layout
left_col, right_col = st.columns(2)

# Data input fields in the left column
with left_col:
    st.subheader("Sales")
    date_input = st.date_input("Date (தேதி)", value=date.today(),format="DD-MM-YYYY")
    total_sales_pos = st.number_input("Total Sales POS ( சேல்ஸ் )", min_value=0, step=100)
    paytm = st.number_input("Paytm (பேடிஎம்)", min_value=0, step=100)
    
    
    # Set opening cash to the previous day's closing cash
    opening_cash = last_closing_cash
    
    # Display opening cash in a read-only text input
    st.markdown(
        f'<div style="color: blue; font-size: 18px; font-weight: bold;">Opening Cash (ஆரம்ப இருப்பு)   : {opening_cash}</div>',
        unsafe_allow_html=True
    )

    st.subheader("Expenses")
    employee_1_advance = st.number_input("Employee 1", min_value=0, step=100)
    employee_2_advance = st.number_input("Employee 2", min_value=0, step=100)
    employee_3_advance = st.number_input("Employee 3", min_value=0, step=100)
    employee_4_advance = st.number_input("Employee 4", min_value=0, step=100)
    cleaning = st.number_input("Cleaning (சுதாகர்)", min_value=0, step=100)

    # Combo box for other expenses
    other_expenses_name = st.selectbox("Other Expenses Name", ["Tea or Snacks ( டீ )", "Flower ( பூ )", "Corporation ( கார்பொரேஷன் )", "Paper ( பேப்பர் )"],label_visibility="collapsed")
    other_expenses_amount = st.number_input("Other Expenses Amount", min_value=0, step=100,label_visibility="collapsed")
    
    # Additional combo box for other expenses
    other_expenses_name_1 = st.selectbox("Other Expenses Name 1", ["Others (வேறு செலவு)", "Flower ( பூ )", "Corporation ( கார்பொரேஷன் )", "Paper ( பேப்பர் )"],label_visibility="collapsed")
    other_expenses_amount_1 = st.number_input("Other Expenses Amount 1", min_value=0, step=100,label_visibility="collapsed")

    # Calculate total expenses
    expenses_shop_total = (
        employee_1_advance
        + employee_2_advance
        + employee_3_advance
        + employee_4_advance
        + cleaning
        + other_expenses_amount
        + other_expenses_amount_1
    )
    
    # Display expenses_shop_total as a read-only text input
    st.markdown(
        f'<div style="color: blue; font-size: 24px; font-weight: bold;">Total Expenses : {expenses_shop_total}</div>',
        unsafe_allow_html=True
    )

# Denominations in the right column
with right_col:
    st.subheader("Denominations")
    denom_500 = st.number_input("500 x ", min_value=0, step=1)
    denom_200 = st.number_input("200 x ", min_value=0, step=1)
    denom_100 = st.number_input("100 x ", min_value=0, step=1)
    denom_50 = st.number_input("50 x ", min_value=0, step=1)
    denom_20 = st.number_input("20 x ", min_value=0, step=1)
    denom_10 = st.number_input("10 x ", min_value=0, step=1)
    denom_5 = st.number_input("5 x ", min_value=0, step=1)

    # Calculate the Denomination Total
    denomination_total = (
        denom_500 * 500
        + denom_200 * 200
        + denom_100 * 100
        + denom_50 * 50
        + denom_20 * 20
        + denom_10 * 10
        + denom_5 * 5
    )

    # Display Denomination Total as a read-only text input
    st.markdown(
        f'<div style="color: blue; font-size: 24px; font-weight: bold;">Total : {denomination_total}</div>',
        unsafe_allow_html=True
    )
    
    cash_withdrawn = st.number_input("Cash Withdrawn (பணம் எடுத்தது)", min_value=0, step=100)

    # Calculate closing cash (denomination total minus cash withdrawn)
    closing_cash = denomination_total - cash_withdrawn
    
    # Display closing cash as a read-only text input
    st.markdown(
        f'<div style="color: blue; font-size: 24px; font-weight: bold;">Closing cash : {closing_cash}</div>',
        unsafe_allow_html=True
    )
    offset = 100
    
    if denomination_total < 500:
        offset = 0
       
    # Total Cash Value
    total_cash = opening_cash + (total_sales_pos - paytm) - expenses_shop_total + offset # Adding Rs. 100 Extra 
    
    # cash difference
    cash_difference = total_cash - denomination_total
    
    #st.text_input("Difference: ", value=f"Difference: {cash_difference}", disabled=True) # Change color based on the value of cash_difference
    if cash_difference > 100:
        text_color = "red"
    elif cash_difference > 0:
        text_color = "blue"
    else:
        text_color = "green"
        
    if cash_difference < -100:
        cash_difference = -100
    
    # Display cash difference with custom color
    # Set font size and make text bold
    font_size = "28px"
    font_weight = "bold"

    # Display cash difference with custom color, bold, and larger font
    st.markdown(
        f'<div style="color: {text_color}; font-size: {font_size}; font-weight: {font_weight};">Difference: {cash_difference}</div>',
        unsafe_allow_html=True
    )

# Submit button
submit_button = st.button("Submit")

# Handle form submission
if submit_button:
    new_row = {
        "Date": date_input,
        "Opening Cash": opening_cash,
        "Expenses Shop": expenses_shop_total,
        "Denomination Total": denomination_total,
        "Total Sales POS": total_sales_pos,
        "Paytm": paytm,
        "Cash Withdrawn": cash_withdrawn,
        "Employee 1": employee_1_advance,
        "Employee 2": employee_2_advance,
        "Employee 3": employee_3_advance,
        "Employee 4": employee_4_advance,
        "Cleaning": cleaning,
        "Other Expenses Name": other_expenses_name,
        "Other Expenses Amount": other_expenses_amount,
        "500": denom_500,
        "200": denom_200,
        "100": denom_100,
        "50": denom_50,
        "20": denom_20,
        "10": denom_10,
        "5": denom_5,
        "Closing Cash": closing_cash,
    }

    # Append the new data to the existing DataFrame
    data = data.append(new_row, ignore_index=True)

    # Save the updated data to the CSV file
    data.to_csv(csv_file, index=False)

    st.success("Data submitted successfully!")
