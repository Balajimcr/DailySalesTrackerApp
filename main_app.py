import streamlit as st
from login_tab import login_tab
from form_tab import form_tab
from accounts_db_tab import accounts_db_tab
from shop_purchase_tab import shop_purchase_tab
from user_authentication import is_logged_in

def main_app():
    st.sidebar.title("Elite Salon - Daily Accounts")
    tab = st.sidebar.radio("Go to", ["Login", "Form", "Daily Accounts Database", "Shop Purchase Account"])

    if tab == "Login":
        login_tab()
    elif is_logged_in():
        if tab == "Form":
            form_tab()
        elif tab == "Daily Accounts Database":
            accounts_db_tab()
        elif tab == "Shop Purchase Account":
            shop_purchase_tab()
    else:
        st.warning("You need to login to access this tab.")

if __name__ == "__main__":
    main_app()
