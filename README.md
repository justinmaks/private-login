# private-login

This is a basic Flask web application with user authentication and a protected tools page.


## Demo

https://stin.lol/

## Features
- User registration and login
- Protected tools page (accessible only to logged-in users)
- SQLite database for user data storage
- Dockerized for easy setup and deployment
- Flash messages for user feedback

## Prerequisites
- Docker installed on your machine
- Docker Compose installed

## Setup

1. Clone the repository

2. Build and run the application:
   ```bash
   docker-compose up --build
   ```

3. Access the app in your browser at:
   ```
   http://localhost:5000
   ```

## Usage

### Register a New User
1. Navigate to `/register` in your browser.
2. Fill out the registration form with a username and password.
3. Submit the form to create your account.

### Log In
1. Navigate to `/login` in your browser.
2. Enter your registered username and password.
3. Access the protected tools page.

### Log Out
Click the "Logout" link in the navigation menu to log out of your account.

## API Routes

### Authentication Routes
- `GET /login`
  - Displays the login page.
- `POST /login`
  - Handles login form submissions and authenticates the user.
- `GET /logout`
  - Logs out the currently logged-in user.
- `GET /register`
  - Displays the registration page.
- `POST /register`
  - Handles registration form submissions and creates a new user account.

### Main Application Routes
- `GET /`
  - Redirects to the login page if the user is not logged in.
- `GET /tools`
  - Displays the protected tools page (accessible only to authenticated users).

## Project Structure
```
my_flask_app/
│
├── app/
│   ├── __init__.py          # Initializes the Flask app
│   ├── auth.py              # Handles authentication routes
│   ├── main.py              # Main application routes
│   ├── models.py            # Database models
│   ├── templates/           # HTML templates
│   │   ├── base.html        # Base layout template
│   │   ├── login.html       # Login page
│   │   ├── register.html    # Registration page
│   │   ├── tools.html       # Protected tools page
│   └── static/              # Static files (CSS, JS, etc.)
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker container configuration
├── docker-compose.yml       # Docker Compose configuration
├── config.py                # Application configuration
└── .gitignore               # Ignored files for Git
```
