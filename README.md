# Flask To-Do List App

A simple To-Do List web application built with **Flask**, featuring **user authentication**, **database migrations**, and **task management**.
This project is ideal for beginners learning Flask or anyone who wants a starter template for a CRUD-based web app.

---

## Table of Contents

* [About](#about)
* [Tech Stack](#tech-stack)
* [Getting Started](#getting-started)

  * [Install Dependencies](#1-install-dependencies)
  * [Set Up the Database](#2-set-up-the-database)
  * [Run the Application](#3-run-the-application)
* [Run with Docker](#run-with-docker)
* [License](#license)

---

## About

This is a lightweight Flask-based To-Do List application supporting:

* User registration & login
* Secure password hashing
* Each user manages their own tasks
* Database migration workflow (Flask-Migrate)

It can be used as a simple productivity tool or as a base project to learn Flask fundamentals.

---

## Tech Stack

* **Python 3**
* **Flask**
* **Flask-Login**
* **Flask-Migrate**
* **SQLAlchemy**
* **HTML / Bootstrap**

---

## Getting Started

Follow these steps to set up and run the project locally.

### 1. Install Dependencies

Make sure Python and pip are installed.

```bash
pip install -r requirements.txt
```

### 2. Set Up the Database

Use Flask-Migrate to initialize and manage migrations:

```bash
flask db init       # Run once, creates migrations folder
flask db migrate    # Generate migration scripts after model changes
flask db upgrade    # Apply latest migrations
```

### 3. Run the Application

**Windows:**

```bash
py app.py
```

**MacOS / Linux:**

```bash
python3 app.py
```

The app should now be accessible at: [http://localhost:5000](http://localhost:5000)

---

## Run with Docker

### Build the Docker image:

```bash
docker build -t flask-todo-app .
```

### Run the container:

```bash
docker run -d -p 5000:5000 flask-todo-app
```

---

## License

This project is open-source and available under the **MIT License**.