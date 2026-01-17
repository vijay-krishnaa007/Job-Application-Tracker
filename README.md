📌 Internship & Job Application Tracker

A Python-based application to efficiently track, manage, and analyze internship and job applications through an interactive Streamlit dashboard.

🔍 Project Overview

Applying to multiple internships and jobs across platforms like LinkedIn, company portals, and referrals quickly becomes difficult to track manually.
This project provides a centralized system to store application details, update statuses, apply filters, and gain insights into application progress.

The application focuses on practical problem-solving, clean data handling, and usability.

✨ Key Features

Add and store internship/job applications in a structured format

Update application status (Applied, Interview, Selected, Rejected, On Hold)

Filter applications by company, role, and status

View all applications in an interactive table

Summary dashboard showing:

Total number of applications

Status-wise distribution

Pending follow-up tracking

Persistent storage using CSV files

🛠️ Tech Stack

Python – Core application logic

Streamlit – Interactive web-based user interface

Pandas – Data manipulation and analysis

CSV – Lightweight persistent data storage

📂 Project Structure
job-application-tracker/
│
├── streamlit_app.py     # Streamlit dashboard
├── app.py               # CLI-based version
├── data/
│   └── applications.csv
└── README.md

🚀 How to Run the Project
1️⃣ Clone the repository
git clone https://github.com/your-username/job-application-tracker.git
cd job-application-tracker

2️⃣ Install dependencies
pip install streamlit pandas

3️⃣ Run the Streamlit application
streamlit run streamlit_app.py


⚠️ Ensure applications.csv is closed while the app is running to avoid permission issues.

📊 Use Case

This application is useful for:

Students applying to internships

Job seekers managing multiple applications

Tracking application progress and follow-ups in one place

🧠 Learning Outcomes

Hands-on Python development

Working with structured data using Pandas

Implementing CRUD operations with persistent storage

Building interactive dashboards using Streamlit

Designing real-world, user-focused software solutions

🔮 Future Enhancements

Database integration (SQLite / PostgreSQL)

User authentication and multi-user support

Automated email reminders for follow-ups

Export reports as Excel or PDF

👤 Author

Bodapati Navaneeth Vijaya Krishna
Bachelor of Technology – Computer Science and Engineering
