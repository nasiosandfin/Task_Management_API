# Task Management API

A Django + Django REST Framework (DRF) backend project that provides a secure API for managing personal tasks.  
This project was developed as a **Backend Engineering Capstone Project** to demonstrate skills in API design, authentication, database management, and deployment.

---

##  Features

- **User Management (CRUD)**  
  - Register, update, and delete user accounts.  
  - Each user manages their own tasks only.  

- **Task Management (CRUD)**  
  - Create, read, update, and delete tasks.  
  - Attributes: Title, Description, Due Date, Priority (Low/Medium/High), Status (Pending/Completed).  
  - Validations: due date must be in the future, priority restricted to defined choices.  

- **Mark Tasks Complete/Incomplete**  
  - Dedicated endpoint to toggle task status.  
  - Completed tasks are locked from editing unless reverted to pending.  
  - Timestamp recorded when marked complete.  

- **Filtering & Sorting**  
  - Filter tasks by status, priority, or due date.  
  - Sort tasks by due date or priority.  

- **Authentication & Permissions**  
  - JWT authentication with `djangorestframework-simplejwt`.  
  - Only authenticated users can access the API.  
  - Tasks are strictly scoped to their owner.  

---

##  Tech Stack

- **Backend Framework:** Django 5.x, Django REST Framework  
- **Database:** SQLite (default), easily switchable to PostgreSQL for production  
- **Authentication:** JWT (JSON Web Tokens)  
- **Deployment:** Heroku / PythonAnywhere  
- **Other Tools:** django-filter for query filtering  

---

##  Project Structure

Task_Management_API/
├── taskmanager/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── tasks/                # App for task management
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── permissions.py
│   └── urls.py
├── requirements.txt
├── Procfile              # For Heroku deployment
└── README.md

Code