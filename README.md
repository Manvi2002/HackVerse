# HackVerse
🚀 HackVerse – Online Hackathon Management System

📌 Project Overview
HackVerse is a web-based Online Hackathon Management System developed using Django and SQLite. The platform automates the complete hackathon workflow including participant registration, team management, hackathon creation, project submission, payment integration, AI-based idea generation, chatbot assistance, evaluation, and leaderboard management.

The system supports three major roles:
Admin
User (Participant)
Judge

HackVerse provides a centralized platform for managing hackathons efficiently with secure authentication and modern AI-powered features.
✨ Features

👨‍💼 Admin Features
Admin Login
Manage Users
Manage Judges
Create / Update / Delete Hackathons
Manage Teams
View Revenue and Payments
View Project Submissions
Monitor Leaderboard
Manage Reports
Logout

👨‍💻 User (Participant) Features
User Registration & Login
Secure JWT Authentication
View Active & Upcoming Hackathons
Register for Hackathons
Create & Manage Teams
Make Payments
Download Invoice PDF
Submit Projects (GitHub Link & ZIP File)
Use AI Idea Generator
Interact with HackVerse Assistant Chatbot
View Leaderboard
Logout

🧑‍⚖️ Judge Features
Judge Login
View Assigned Hackathons
View Teams & Participants
Access Submitted Projects
Evaluate Projects
Give Scores & Feedback
View Leaderboard
Logout

🤖 AI Features

💡 AI Idea Generator
Generates:
Project Name
Problem Statement
Proposed Solution
Suggested Technologies
based on user-provided themes.

🤖 HackVerse Assistant Chatbot
Provides instant support
Helps users navigate the platform
Answers hackathon-related queries
Supports Admin, Users, and Judges

🛠️ Technologies Used
Frontend
HTML5
CSS3
Bootstrap
JavaScript
Backend
Python
Django Framework
Database
SQLite
Authentication
JWT (JSON Web Token)
Payment Gateway
Razorpay (Test Mode)

📂 Modules
Profile Module
Hackathon Module
My Teams Module
AI Idea Generator Module
Chatbot Module
Payment Module
Project Submission & Evaluation Module
Leaderboard Module
Report Module

⚙️ System Requirements
Hardware Requirements
Processor: Intel i3 or above
RAM: 4 GB or above
Storage: 256 GB
Software Requirements
Windows / Linux
Python 3.x
Django
SQLite
Visual Studio Code
Web Browser (Chrome, Edge, Firefox)

📥 Installation Steps

1️⃣ Clone Repository
git clone <repository-url>
2️⃣ Move to Project Directory
cd hackverse
3️⃣ Create Virtual Environment
python -m venv venv
4️⃣ Activate Virtual Environment
Windows
venv\Scripts\activate
Linux / Mac
source venv/bin/activate
5️⃣ Install Dependencies
pip install -r requirements.txt
6️⃣ Run Migrations
python manage.py makemigrations
python manage.py migrate
7️⃣ Create Superuser
python manage.py createsuperuser
8️⃣ Run Server
python manage.py runserver
🌐 Access Application

💳 Payment Integration
HackVerse uses Razorpay Test Mode for payment processing.
Features:
Registration Fee Payment
Payment Status Tracking
Invoice Generation PDF

🔐 Security Features
JWT Authentication
Password Hashing
Role-Based Access Control
Secure Session Management

📊 Future Enhancements
Cloud Deployment
Mobile Application
AI-Based Project Evaluation
Real-Time Notifications
Advanced Analytics Dashboard
Team Matching Recommendation System

👨‍💻 Developed By

Manvi Agrawal
Master of Computer Application (MCA)

📚 References
Django Documentation
Razorpay Documentation
Bootstrap Documentation
SQLite Documentation
JWT Authentication Guide

📄 License
This project is developed for educational and academic purposes.
