# Productivity Notes App for Backend

## Description

A secure Flask API backend for a productivity app where users can create, read, update, and delete their personal notes. Implements JWT-based authentication to ensure users can only access their own data. Supports pagination on the notes index endpoint.

## Installation

1. Ensure you have Python 3 + and above.
2. Install pipenv if not already installed: `pip install pipenv`
3. Clone the repository and navigate to the project directory.
4. Run `pipenv install` to install dependencies.
5. Activate the virtual environment: `pipenv shell`  

     OR I SAW THIS 
     you can write this command to create virtual evnvironment

     '''python3 -m venv .venv'''  

     and this to activate the venv

     '''source .venv/bin/activate'''


     
6. Initialize the database: `flask db init` (if not already done)
7. Create and apply migrations: `flask db migrate && flask db upgrade`
8. Seed the database with sample data: `python seed.py`

## Run Instructions

1. Ensure you are in the pipenv shell.
2. Run the application: `flask run`
3. The server will start on `http://127.0.0.1:5000/`

## Endpoints

### Authentication
- `POST /signup` - Register a new user. Body: `{ "username": "string", "password": "string" }`
- `POST /login` - Login and receive JWT token. Body: `{ "username": "string", "password": "string" }`. Returns: `{ "access_token": "jwt_token" }`
- `GET /me` - to get current user information. Requires JWT token in Authorization header.

### Notes
- `GET /notes` - Get a list of user's notes.
- `POST /notes` - Create a new note. Body: `{ "title": "string", "content": "string" }`
- `GET /notes/<id>` - Get a specific note by ID
- `PATCH /notes/<id>` - Update a note. Body: `{ "title": "string", "content": "string" }` (partial update)
- `DELETE /notes/<id>` - Delete a note by the ID




