import streamlit as st
import pandas as pd
from database import create_tables, run_query

st.set_page_config(page_title="HospConnect", layout="wide")
create_tables()

if 'user' not in st.session_state:
    st.session_state.user = None

def login_ui():
    st.title("🏥 Hospital Management System")
    role = st.sidebar.selectbox("Login as", ["Admin", "Doctor", "Patient"])
    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")
    
    if st.button("Login"):
        col_name = "username" if role == "Admin" else "name"
        query = f"SELECT id, {col_name} FROM {role} WHERE username=? AND password=?"
        result = run_query(query, (user, pw), fetch=True)
        
        if result:
            st.session_state.user = {"id": result[0][0], "name": result[0][1], "role": role}
            st.rerun()
        else:
            st.error("Invalid Credentials")

def admin_panel():
    st.header("Admin Dashboard")
    t1, t2, t3 = st.tabs(["Register Doctor", "Register Patient", "View Records"])
    
    with t1:
        d_name = st.text_input("Doctor Name")
        d_uname = st.text_input("Doctor Username")
        d_pwd = st.text_input("Doctor Password", type="password")
        if st.button("Add Doctor"):
            run_query("INSERT INTO Doctor (name, username, password) VALUES (?,?,?)", (d_name, d_uname, d_pwd))
            st.success(f"Doctor {d_name} added!")

    with t2:
        p_name = st.text_input("Patient Name")
        p_uname = st.text_input("Patient Username")
        p_pwd = st.text_input("Patient Password", type="password")
        if st.button("Add Patient"):
            run_query("INSERT INTO Patient (name, username, password) VALUES (?,?,?)", (p_name, p_uname, p_pwd))
            st.success(f"Patient {p_name} added!")

    with t3:
        st.subheader("Doctors List")
        docs = run_query("SELECT id, name, status FROM Doctor", fetch=True)
        st.dataframe(pd.DataFrame(docs, columns=["ID", "Name", "Status"]), use_container_width=True)
        
        st.subheader("Patients List")
        pats = run_query("SELECT id, name, username FROM Patient", fetch=True)
        st.dataframe(pd.DataFrame(pats, columns=["ID", "Name", "Username"]), use_container_width=True)

def doctor_panel():
    st.header(f"Dr. {st.session_state.user['name']}'s Portal")
    status = st.selectbox("Set My Availability", ["available", "busy"])
    if st.button("Update Status"):
        run_query("UPDATE Doctor SET status=? WHERE id=?", (status, st.session_state.user['id']))
        st.success("Status updated!")

    st.subheader("Upcoming Appointments")
    query = """SELECT Patient.name, Appointment.date, Appointment.time 
               FROM Appointment JOIN Patient ON Appointment.p_id = Patient.id 
               WHERE Appointment.d_id = ?"""
    apps = run_query(query, (st.session_state.user['id'],), fetch=True)
    st.table(pd.DataFrame(apps, columns=["Patient Name", "Date", "Time"]))

def patient_panel():
    st.header(f"Welcome, {st.session_state.user['name']}")
    
    st.subheader("Book an Appointment")
    docs = run_query("SELECT id, name FROM Doctor WHERE status='available'", fetch=True)
    if docs:
        doc_map = {d[1]: d[0] for d in docs}
        sel_doc = st.selectbox("Choose a Doctor", list(doc_map.keys()))
        date = st.date_input("Select Date")
        time = st.time_input("Select Time")
        
        if st.button("Request Appointment"):
            run_query("INSERT INTO Appointment (p_id, d_id, date, time) VALUES (?,?,?,?)", 
                      (st.session_state.user['id'], doc_map[sel_doc], str(date), str(time)))
            st.success("Appointment Booked!")
    else:
        st.warning("No doctors are currently available.")

if st.session_state.user is None:
    login_ui()
else:
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()
    
    role = st.session_state.user['role']
    if role == "Admin": admin_panel()
    elif role == "Doctor": doctor_panel()
    elif role == "Patient": patient_panel()