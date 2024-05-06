import streamlit as st
import pandas as pd
import random
from data_management import load_data, load_employee_names
from ui_helpers import Text, tabs_font_css
from datetime import date, datetime, timedelta
from data_management import csv_file, employee_csv

def form_tab():
    # Initialize data, last closing cash, and employee names
    data, last_closing_cash = load_data()
    employee_names = load_employee_names()

    st.title("Elite Salon Daily Accounts")

    st.write(tabs_font_css, unsafe_allow_html=True)

    # Create a two-column layout
    left_col, right_col = st.columns(2)

    # Data input fields in the left column
    with left_col:
        st.subheader("Sales")
        #Date_Label = '<p style="color:Black; font-size: 24px;"></p>'
        date_input = st.date_input(Text("Date (தேதி)"), value=date.today(), format="DD-MM-YYYY")
        opening_cash = st.number_input(Text("Opening Cash (ஆரம்ப இருப்பு)"),value=last_closing_cash, min_value=0, step=100)
        total_sales_pos = st.number_input(Text("Total Sales POS ( சேல்ஸ் )"), min_value=0, step=100)
        paytm = st.number_input(Text("Paytm (பேடிஎம்)"), min_value=0, step=100)

        # Expenses fields
        st.subheader("Expenses")
        employee_1_advance = st.number_input(Text(employee_names[0]), min_value=0, step=100)
        employee_2_advance = st.number_input(Text(employee_names[1]), min_value=0, step=100)
        employee_3_advance = st.number_input(Text(employee_names[2]), min_value=0, step=100)
        employee_4_advance = st.number_input(Text(employee_names[3]), min_value=0, step=100)
        cleaning = st.number_input(Text("Cleaning"), min_value=0, step=100)

        # Combo box for other expenses with hidden label
        other_expenses_name = st.selectbox(Text("Other Expenses Name"), 
                                        ["Tea or Snacks ( டீ )", "Flower ( பூ )", "Corporation ( கார்பொரேஷன் )", "Paper ( பேப்பர் )"],
                                        label_visibility="collapsed")
        other_expenses_amount = st.number_input("Other Expenses Amount", min_value=0, step=100, label_visibility="collapsed")

        other_expenses_name_1 = st.selectbox(Text("Other Expenses Name 1"), 
                                            ["Others (வேறு செலவு)", "Flower ( பூ )", "Corporation ( கார்பொரேஷன் )", "Paper ( பேப்பர் )"],
                                            label_visibility="collapsed")
        other_expenses_amount_1 = st.number_input("Other Expenses Amount 1", min_value=0, step=100, label_visibility="collapsed")

        # Calculate and display total expenses
        expenses_shop_total = (
            employee_1_advance
            + employee_2_advance
            + employee_3_advance
            + employee_4_advance
            + cleaning
            + other_expenses_amount
            + other_expenses_amount_1
        )
        st.markdown(
            f'<div style="color: blue; font-size: 24px; font-weight: bold;">Total Expenses: ₹{expenses_shop_total}</div>',
            unsafe_allow_html=True
        )


    # Denominations in the right column
    with right_col:
        st.subheader("Denominations")
        denom_500 = st.number_input(Text("500 x"), min_value=0, step=1)
        denom_200 = st.number_input(Text("200 x"), min_value=0, step=1)
        denom_100 = st.number_input(Text("100 x"), min_value=0, step=1)
        denom_50  = st.number_input(Text("50 x"), min_value=0, step=1)
        denom_20  = st.number_input(Text("20 x"), min_value=0, step=1)
        denom_10  = st.number_input(Text("10 x"), min_value=0, step=1)
        denom_5   = st.number_input(Text("5 x"), min_value=0, step=1)

        # Calculate the denomination total
        denomination_total = (
            denom_500 * 500
            + denom_200 * 200
            + denom_100 * 100
            + denom_50 * 50
            + denom_20 * 20
            + denom_10 * 10
            + denom_5 * 5
        )

        st.markdown(
            f'<div style="color: blue; font-size: 24px; font-weight: bold;">Total: ₹{denomination_total}</div>',
            unsafe_allow_html=True
        )

        cash_withdrawn = st.number_input(Text("Cash Withdrawn (பணம் எடுத்தது)"), min_value=0, step=100)

        # Calculate closing cash and display
        closing_cash = denomination_total - cash_withdrawn
        st.markdown(
            f'<div style="color: blue; font-size: 24px; font-weight: bold;">Closing Cash: ₹{closing_cash}</div>',
            unsafe_allow_html=True
        )

        # Offset for denominations
        offset = 100
        if denomination_total < 500:
            offset = 0
        
        # Calculate total cash and cash difference
        total_cash = opening_cash + (total_sales_pos - paytm) - expenses_shop_total + offset
        cash_difference = total_cash - denomination_total
        
        cash_difference_masked = cash_difference

        # Set text color based on cash difference
        if cash_difference > 100:
            text_color = "red"
        elif cash_difference > 0:
            text_color = "blue"
        else:
            text_color = "green"
            
        # Limit negative cash difference to -100
        if cash_difference < -100:
            cash_difference_masked = random.randint(1, 10) * 10
            
        st.markdown(
            f'<div style="color: blue; font-size: 24px; font-weight: bold;">Total Sales: ₹{total_sales_pos}</div>',
            unsafe_allow_html=True
        )
        
        st.markdown(
            f'<div style="color: blue; font-size: 24px; font-weight: bold;">Cash: ₹{total_sales_pos - paytm}</div>',
            unsafe_allow_html=True
        )
        
        st.markdown(
            f'<div style="color: blue; font-size: 24px; font-weight: bold;">Paytm: ₹{paytm}</div>',
            unsafe_allow_html=True
        )
        
        st.markdown(
            f'<div style="color: blue; font-size: 24px; font-weight: bold;">Expenses: ₹{expenses_shop_total}</div>',
            unsafe_allow_html=True
        )
        
        st.markdown(
            f'<div style="color: blue; font-size: 24px; font-weight: bold;">Total Cash: ₹{total_cash}</div>',
            unsafe_allow_html=True
        )
        
        # Display cash difference with custom font size and color
        font_size = "28px"
        font_weight = "bold"
        st.markdown(
            f'<div style="color: {text_color}; font-size: {font_size}; font-weight: {font_weight};">Difference: ₹{cash_difference_masked}</div>',
            unsafe_allow_html=True
        )

    # Submit button to handle form submission
    submit_button = st.button("Submit")

    if submit_button:
        new_row = {
            "Date": date_input.strftime('%d-%m-%Y'),  # Only use the date part
            "Opening Cash": opening_cash,
            "Expenses Shop": expenses_shop_total,
            "Denomination Total": denomination_total,
            "Total Cash": total_cash,
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
            "Other Expenses Name_1": other_expenses_name_1,
            "Other Expenses Amount_1": other_expenses_amount_1,
            "500": denom_500,
            "200": denom_200,
            "100": denom_100,
            "50": denom_50,
            "20": denom_20,
            "10": denom_10,
            "5": denom_5,
            "Cash Difference": cash_difference,
            "Closing Cash": closing_cash,
        }
        
        # Default to True indicating data is valid to submit
        Pass = True

        # Check if cash_withdrawn is greater than the available cash in denominations
        if cash_withdrawn > denomination_total:
            Pass = False
            st.markdown(
                f'<div style="color: Red; font-size: {font_size}; font-weight: {font_weight};"> [Error] Cash Withdrawn is wrong! {cash_withdrawn} > {denomination_total} </div>',
                unsafe_allow_html=True
            )
            
        if abs(cash_difference) > 1000:
            Pass = False
            st.markdown(
                f'<div style="color: Red; font-size: {font_size}; font-weight: {font_weight};"> [Error] High Cash Difference : {cash_difference}! Call Owner  </div>',
                unsafe_allow_html=True
            )

        # If the checks passed, proceed to add new data and save it
        if Pass:
            # Use pd.concat() to add the new row to the existing data
            data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)

            # Append the new data to the CSV file without overwriting, with proper line terminators
            with open(csv_file, 'a', encoding='utf-8', newline='') as f:
                # Write the data to CSV without header if appending
                data.tail(1).to_csv(f, header=f.tell() == 0, index=False, lineterminator='\n')

            st.success("Data submitted successfully!")
            st.balloons()
