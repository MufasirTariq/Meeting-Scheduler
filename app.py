'''This Flask application is a web-based system that provides user authentication, email verification, password reset functionality, and a dashboard for logged-in users. Here's a brief breakdown of what each section of the code does:

### 1. **Environment Setup**
   - The `load_dotenv()` function loads environment variables from a `.env` file. These variables include sensitive information like database URIs, email server credentials, and secret keys.
   
### 2. **Flask App Initialization**
   - The Flask application (`app`) is created, and various configurations are set up, such as connecting to a 
   MongoDB database (`MONGO_URI`), setting secret keys (`FLASK_SECRET_KEY`, `JWT_SECRET_KEY`), and configuring email services for password reset functionality.

### 3. **JWT Authentication Setup**
   - `JWTManager` is initialized for handling user authentication via JSON Web Tokens (JWT), which will secure API routes and manage user sessions.

### 4. **Bcrypt & Email Setup**
   - The `bcrypt` extension is initialized for securely hashing passwords.
   - The `mail` extension is set up with the required SMTP configurations to send emails (for verification and password reset).

### 5. **URLSafeTimedSerializer**
   - This is used for generating and validating time-sensitive tokens, such as for email verification and password reset links. These tokens expire after a certain period (1 hour in this case).

### 6. **Routes (URLs) and Views**
   - **Login Page (`/`)**: The main login page is rendered where users can enter credentials to log in.
   - **Email Verification (`/verify`)**: Displays a page for email verification instructions.
   - **Register (`/register/<token>`)**: Allows a user to register after verifying the email token. If the token is expired or invalid, an error message is shown.
   - **Forgot Password (`/forgetpassword`)**: Displays a page for users to request a password reset.
   - **Reset Password (`/resetpassword/<token>`)**: Allows users to reset their password after validating the reset token. If the token is expired or invalid, an error message is shown.
   - **Logout (`/logout`)**: Logs out the user by removing the `user_id` from the session.
   - **Dashboard (`/dashboard`)**: After successful login, the user is redirected to the dashboard page, where user details and lists are displayed.

### 7. **Database & Routes Initialization**
   - The `initialize_db()` function sets up the MongoDB database connection.
   - The `initialize_routes()` and `initialize_meeting_routes()` functions import and set up routes for user and meeting-related actions.

### 8. **Running the App**
   - The app runs on the local development server at port `1234` in debug mode, which helps during development by automatically reloading the server upon changes.

### Summary
This application provides basic authentication, email-based registration, and password reset workflows. 
It integrates with a MongoDB database and uses JWT for secure user sessions. The setup ensures that user data, 
authentication tokens, and sensitive operations (like password reset) are handled securely.'''

from flask import Flask, render_template, session
from flask_jwt_extended import JWTManager
from routes.user_routes import initialize_routes
from routes.meeting_routes import initialize_meeting_routes
from database.db import initialize_db
from extension import bcrypt, mail
from itsdangerous import URLSafeTimedSerializer
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# MongoDB Configuration
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
initialize_db(app)  # Database initialize

# Initialize routes
initialize_routes(app)  # user routes initialize
initialize_meeting_routes(app)  # meeting routes initialize

# Initialize Bcrypt
bcrypt.init_app(app)

# JWT Configuration
app.secret_key = os.getenv('FLASK_SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')  

jwt = JWTManager(app)

# Mail Configuration
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

mail.init_app(app)

# URLSafeTimedSerializer Secret
s = URLSafeTimedSerializer(os.getenv('URL_SAFE_TIMED_SECRET'))

@app.route('/')
def loginPage():
    return render_template('login.html')

@app.route('/verify')
def verify():
    return render_template('verify_email.html')

@app.route('/register/<token>')
def register(token):
    email = s.loads(token, salt='email-confirmation', max_age=3600)
    if email:
        return render_template('register.html', email=email)
    else:
        return {"Verification":"Failed or link expired, Try Again!"}

@app.route('/forgetpassword')
def forgotpassowrd():
    return render_template('forgetpassword.html')

@app.route('/resetpassword/<token>')
def resetpassword(token):
    user_id = s.loads(token, salt='password-forgot', max_age=3600)
    if user_id:
        return render_template('resetpassword.html', user_id=user_id)
    else:
        return {"message":"Failed or link expired, Try Again!"}

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_list', None)
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if session.get('user') and session.get('user_list'):
        user = session.get('user')
        user_list = session.get('user_list')
        return render_template('dashboard.html', user=user, user_list=user_list)

if __name__ == '__main__':
    app.run(debug=True, port=1234)
