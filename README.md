# 🏥 HospConnect: Hospital Management System

A full-stack, role-based web application designed to streamline healthcare workflows. This project integrates a reactive **Streamlit** frontend with a persistent **SQLite** relational backend.

## 🚀 Overview
HospConnect provides a digital portal for hospital operations, managing the interactions between Admins, Doctors, and Patients. It is built with a modular architecture that separates database logic from the user interface, ensuring the system is maintainable and ready for future scaling.

## 🛠️ Tech Stack
* **Frontend:** Streamlit (Python)
* **Backend:** SQLite (Relational Database)
* **Database Driver:** `sqlite3`
* **Data Handling:** Pandas

## 🔑 Key Features
* **Admin Dashboard:** Register new doctors and patients, and oversee hospital-wide records.
* **Doctor Portal:** Manage professional availability status and view assigned patient appointments via SQL Joins.
* **Patient Portal:** Browse available doctors and book appointments for specific dates and times.
* **Role-Based Access Control (RBAC):** Distinct login workflows ensure that users only access data relevant to their role.

## 📂 Project Structure
```text
hospital_system/
├── app.py           # Main Streamlit UI and Page Routing
├── database.py      # SQL Schema and Database Logic
├── requirements.txt # Project Dependencies
└── README.md        # Documentation
