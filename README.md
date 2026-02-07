# Python Full-Stack Task Manager

A lightweight, full-stack web application built with a Python (Flask) backend and a vanilla JavaScript/Tailwind CSS frontend. This project demonstrates basic CRUD (Create, Read, Update, Delete) operations, RESTful API design, and database persistence using SQLite.

Features

Add Tasks: Create new tasks that are saved instantly.

Toggle Status: Mark tasks as complete or pending with a checkbox.

Delete Tasks: Remove tasks from the database.

Persistent Storage: Uses SQLite to ensure your data stays put.

Responsive Design: Styled with Tailwind CSS for a clean look on mobile and desktop.

Tech Stack

Backend: Python, Flask, Flask-CORS, SQLite

Frontend: HTML5, JavaScript (Fetch API), Tailwind CSS

Deployment: Gunicorn (WSGI Server)

Local Setup

Clone the repository:

git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
cd YOUR_REPO_NAME


Install dependencies:

pip install -r requirements.txt


Run the application:

python task_manager.py


Access the app:
Open your browser and navigate to http://127.0.0.1:5000

Deployment (Render)
To host this on Render:

Create a new Web Service and connect your GitHub repo.

Build Command: pip install -r requirements.txt

Start Command: gunicorn task_manager:app

Environment Variables: None required for the basic setup.

License:
This project is open-source and available under the MIT License.