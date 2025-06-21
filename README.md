# Flask To-Do List App

## Table of Contents

- [About](#about)
- [Getting Started](#getting-started)

## About

This is a simple Flask-based To-Do List application that includes user authentication and database integration. It allows users to register, log in, and manage their personal to-do items.

## Getting Started

Follow these steps to set up and run the application:

### 1. Install Dependencies

Make sure you have Python and pip installed. Then, install the required packages:

```bash
pip install -r requirements.txt
```

### 2. Set Up the Database

```bash
flask db init       # Run this only once to initialize migrations
flask db migrate    # Run this every time you modify the models
flask db upgrade    # Apply the latest migrations
```

### 3. Run the application

```bash
python app.py
```
