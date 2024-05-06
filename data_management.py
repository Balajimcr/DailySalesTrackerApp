import pandas as pd
from datetime import datetime
import pandas as pd  # Make sure pandas is imported

UserDirectoryPath = "Data/EliteSalonLalgudi/"

csv_file = UserDirectoryPath +"database_collection.csv"
employee_csv = UserDirectoryPath +"Employee_data.csv"
employee_salary_Advance_bankTransfer_csv = UserDirectoryPath +"employee_salary_Advance_bankTransfer_data.csv"
employee_salary_data_csv = UserDirectoryPath +"employee_salary_data.csv"

def load_employee_names():
    try:
        employee_data = pd.read_csv(employee_csv)
        employee_names = employee_data["Name"].tolist()
    except (FileNotFoundError, IndexError):
        st.error("Employee names file not found! Please ensure the file exists.")
        employee_names = ["Kamal","Gopal","Arumugam","Employee 4"]
    return employee_names

def load_data():
    try:
        data = pd.read_csv(csv_file)
        data['Date'] = pd.to_datetime(data['Date'], errors='coerce', dayfirst=True)
        data.sort_values(by='Date', inplace=True)
        today_date = datetime.combine(datetime.today().date(), datetime.min.time())
        filtered_data = data[data['Date'] < today_date].copy()
        if not filtered_data.empty:
            last_closing_cash = filtered_data["Closing Cash"].iloc[-1]
        else:
            last_closing_cash = 0
    except (FileNotFoundError, IndexError):
        data = pd.DataFrame(columns=[
            "Date", "Opening Cash", "Expenses Shop", "Denomination Total","Total Cash",
            "Total Sales POS", "Paytm", "Cash Withdrawn", "Employee 1", 
            "Employee 2", "Employee 3", "Employee 4", "Cleaning", 
            "Other Expenses Name", "Other Expenses Amount", 
            "Other Expenses Name_1", "Other Expenses Amount_1", 
            "500", "200","100", "50", "20", "10", "5","Cash Difference",
            "Closing Cash"
        ])
        last_closing_cash = 0
    return data, last_closing_cash

