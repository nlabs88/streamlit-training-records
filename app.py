import os
from dotenv import load_dotenv
import streamlit as st
from supabase import create_client
import pandas as pd

# Load .env file
load_dotenv()

# Load credentials from environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Connect to Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def view_employees():
    st.title("Employee Management")

    # Fetch employee data
    response = supabase.table("Employees").select("*").execute()
    employees = pd.DataFrame(response.data)

    st.dataframe(employees)

    # Add new employee
    with st.form("add_employee"):
        emp_id = st.text_input("Employee ID")
        emp_name = st.text_input("Employee Name")
        hire_date = st.date_input("Hire Date")

        if st.form_submit_button("Add Employee"):
            supabase.table("Employees").insert(
                {"ID": emp_id, "Name": emp_name, "HireDate": hire_date}
            ).execute()
            st.success("Employee added!")


def sign_employee_into_course():
    st.title("Sign Employee Into Course")

    # Fetch data
    employees = supabase.table("Employees").select("ID, Name").execute().data
    courses = supabase.table("EmployeeActivityType").select("ID, EAT_ActivityType").execute().data

    employee_selection = st.selectbox("Select Employee", [e["ID"] for e in employees])
    course_selection = st.selectbox("Select Course", [c["ID"] for c in courses])
    activity_date = st.date_input("Date")
    hours = st.number_input("Hours", min_value=0.5, step=0.5)

    if st.button("Sign In"):
        supabase.table("EmployeeActivity").insert({
            "EA_Adm_num": employee_selection,
            "EA_Activity": course_selection,
            "EA_ActivityDate": activity_date,
            "EA_ActivityHours": hours
        }).execute()
        st.success("Employee signed into course!")


def view_employee_history():
    st.title("Employee Course History")

    employee_id = st.text_input("Enter Employee ID")
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")

    if st.button("Fetch History"):
        query = (
            supabase.table("EmployeeActivity")
            .select("EA_Adm_num, EA_Activity, EA_ActivityDate, EA_ActivityHours")
            .eq("EA_Adm_num", employee_id)
            .gte("EA_ActivityDate", str(start_date))
            .lte("EA_ActivityDate", str(end_date))
            .execute()
        )

        df = pd.DataFrame(query.data)
        st.dataframe(df)


def view_course_attendance():
    st.title("Course Attendance")

    course_id = st.text_input("Enter Course ID")
    date = st.date_input("Date")

    if st.button("Fetch Attendance"):
        query = (
            supabase.table("EmployeeActivity")
            .select("EA_Adm_num, EA_Activity, EA_ActivityDate")
            .eq("EA_Activity", course_id)
            .eq("EA_ActivityDate", str(date))
            .execute()
        )

        df = pd.DataFrame(query.data)
        st.dataframe(df)

