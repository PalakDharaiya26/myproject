# User Authentication System

## Project Overview

This is a Django-based User Authentication System that allows users to register, log in, manage their profile, and securely log out. The project uses a custom user model and includes an admin panel for managing registered users.

## Features

 User Registration
 User Login
 Dashboard
 Profile Management

   Update Username
   Update Mobile Number
   Update Address
   Change Password
   Email is read-only and cannot be changed
   User Logout
   Django Admin Panel to manage registered users

## Tech Stack

 Python
 Django
 SQLite
 HTML
 CSS

## Prerequisites

Before running the project, make sure you have the following installed:

Python 3.x
pip
Git (optional)

## Installation

## 1. Clone the Repository

```bash
git clone <git clone https://github.com/PalakDharaiya26/myproject.git>
cd myproject
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

**Windows**

```bash
.venv\Scripts\activate
```

**Linux/macOS**
```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Apply Database Migrations

```bash
python manage.py migrate
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

### 7. Open the Application

Visit:

```text
http://127.0.0.1:8000/accounts/login/
```

## Project Workflow

1. A new user creates an account using the Registration page.
2. The user logs in using a valid username and password.
3. After successful login, the user is redirected to the Dashboard.
4. The Dashboard provides navigation to the Profile page and Logout.
5. From the Profile page, the user can:

    Update Username
    Update Mobile Number
    Update Address
    Change Password
    View Email (read-only)
6. The user can securely log out.
7. The Django Admin Panel displays all registered users and their details.

## Project Structure

```text
myproject/
│── accounts/
│── templates/
│── static/
│── manage.py
│── requirements.txt
│── README.md
```

## Admin Panel

To access the Django Admin Panel, open:

```text
http://127.0.0.1:8000/admin/
```

Log in using a superuser account created with:

```bash
python manage.py createsuperuser
```
