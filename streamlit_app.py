import streamlit as st
from employee_salary_tab import employee_salary_tab
from form_tab import form_tab
from ui_helpers import Text
from accounts_db_tab import accounts_db_tab
from shop_purchase_tab import shop_purchase_tab
from employee_details import employee_details_tab
from user_authentication import is_logged_in
from user_authentication import login

def main_app():
    st.sidebar.title("Elite Salon - Daily Accounts")
    tab = st.sidebar.radio("Go to", ["Login", Text("Form"), "Daily Accounts Database", "Shop Purchase Account","Employee Details","Employee Salary Account"])

    if tab == "Login":
        login()
    elif is_logged_in():
        if tab == Text("Form"):
            form_tab()
        elif tab == "Daily Accounts Database":
            accounts_db_tab()
        elif tab == "Shop Purchase Account":
            shop_purchase_tab()
        elif tab == "Employee Salary Account":
            employee_salary_tab()
        elif tab == "Employee Details":
            employee_details_tab()
    else:
        st.warning("You need to login to access this tab.")

if __name__ == "__main__":
    main_app()
