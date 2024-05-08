import streamlit as st
import pandas as pd
import random
from data_management import load_data, load_employee_names
from ui_helpers import Text, tabs_font_css,display_text
from datetime import date, datetime, timedelta
from data_management import csv_file

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
        date_input      = st.date_input(Text("Date (தேதி)"), value=date.today(), format="DD-MM-YYYY")
        opening_cash    =  st.number_input(Text("Opening Cash (ஆரம்ப இருப்பு)"),value=last_closing_cash, min_value=0, step=100)
        total_sales_pos = st.number_input(Text("Total Sales POS ( சேல்ஸ் )"), min_value=0, step=100)
        paytm           = st.number_input(Text("Paytm (பேடிஎம்)"), min_value=0, step=100)

        # Expenses fields
        st.subheader("Expenses")
        # Generate number inputs for employee advances using list comprehension
        employee_advances = [st.number_input(Text(name), min_value=0, step=100) for name in employee_names]

        # Generate number input for cleaning expenses
        cleaning = st.number_input(Text("Cleaning"), min_value=0, step=100)

       # Unified list of other expenses options
        other_expenses_options = ["Tea or Snacks ( டீ )", "Others (வேறு செலவு)", "Flower ( பூ )", "Corporation ( கார்பொரேஷன் )", "Paper ( பேப்பர் )"]

        # Initialize a list to collect the amounts of other expenses
        other_expenses_names = []
        other_expenses = []

        # Loop through a range to create multiple expense inputs using an offset
        number_of_expense_inputs = 2  # Adjust the number as needed
        for idx in range(number_of_expense_inputs):
            offset = idx + 1  # Start indexing from 1
            name_label = f"Other Expenses Name {offset}"
            amount_label = f"Other Expenses Amount {offset}"
            expense_name = st.selectbox(Text(name_label), other_expenses_options,index=idx, label_visibility="collapsed")
            expense_amount = st.number_input(amount_label, min_value=0, step=100, label_visibility="collapsed")
            other_expenses.append(expense_amount)
            other_expenses_names.append(expense_name)

        # Calculate and display total expenses
        expenses_shop_total = sum(employee_advances) + cleaning + sum(other_expenses)

        display_text(f"Total Expenses: ₹{expenses_shop_total}")


    # Denominations in the right column
    with right_col:
        st.subheader("Denominations")
        # Define denominations and their corresponding values
        denominations = [500, 200, 100, 50, 20, 10, 5]

        # Create a dictionary to store user input for each denomination
        denomination_counts = {denom: st.number_input(Text(f"{denom} x"), min_value=0, step=1) for denom in denominations}

        # Calculate the denomination total using list comprehension
        denomination_total = sum(count * value for count, value in denomination_counts.items())

        display_text(f"Total: ₹{denomination_total}")

        cash_withdrawn = st.number_input(Text("Cash Withdrawn (பணம் எடுத்தது)"), min_value=0, step=100)

        # Calculate closing cash and display
        closing_cash = denomination_total - cash_withdrawn
        
        display_text(f"Closing Cash: ₹{closing_cash}")

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
        
        display_text(f"Total Sales: ₹{total_sales_pos}")
        display_text(f"Cash: ₹{total_sales_pos - paytm}")
        display_text(f"Paytm: ₹{paytm}")
        display_text(f"Expenses: ₹{expenses_shop_total}")
        display_text(f"Total Cash: ₹{total_cash}")
        display_text(f"Closing Cash: ₹{closing_cash}")
        # Display cash difference with custom font size and color
        display_text(f"Difference: ₹{cash_difference_masked}",color=text_color,font_size ="28px")

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
            "Employee 1": employee_advances[0],
            "Employee 2": employee_advances[1],
            "Employee 3": employee_advances[2],
            "Employee 4": employee_advances[3],
            "Cleaning": cleaning,
            "Other Expenses Name": other_expenses_names[0],
            "Other Expenses Amount": other_expenses[0],
            "Other Expenses Name_1": other_expenses_names[1],
            "Other Expenses Amount_1": other_expenses[1],
            "500": denomination_counts[500],
            "200": denomination_counts[200],
            "100": denomination_counts[100],
            "50": denomination_counts[50],
            "20": denomination_counts[20],
            "10": denomination_counts[10],
            "5": denomination_counts[5],
            "Cash Difference": cash_difference,
            "Closing Cash": closing_cash,
        }
        
        # Default to True indicating data is valid to submit
        Pass = True

        # Check if cash_withdrawn is greater than the available cash in denominations
        if cash_withdrawn > denomination_total:
            Pass = False
            display_text(f"[Error] Cash Withdrawn is wrong! {cash_withdrawn} > {denomination_total}",color="red",font_size ="28px")
            
        if abs(cash_difference) > 1000:
            Pass = False
            display_text(f"[Error] High Cash Difference : {cash_difference}! Call Owner",color="red",font_size ="28px")
            
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
