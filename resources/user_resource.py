'''Here’s a summary of what the provided code does:

### **UserVerifyApi Class** (Handles email verification):

- **`post()` method**:
  - Accepts an `email` as a URL parameter and checks if a user with that email already exists using `UserModel.find_by_email()`.
  - If the user exists, it returns a message saying "This email already exists."
  - If the user doesn't exist, it generates a token using `itsdangerous.URLSafeTimedSerializer` for email verification.
  - Sends a verification email containing a link (generated using `url_for`) to the provided email address using `Flask-Mail`.
  - The email contains a link to the registration page, where the user can verify their email.

### **UserApi Class** (Handles user creation and listing):

- **`get()` method**:
  - Retrieves all users from the database using `UserModel.find_all()`.
  - Stores the list of users in the session (`session['user_list']`) and returns the list of users as a response.

- **`post()` method**:
  - Accepts JSON input with user details (email, password, username, role).
  - Validates that all required fields are provided.
  - Hashes the password using `Flask-Bcrypt` and creates a new user with the provided details.
  - Saves the new user to the database and returns a success message with HTTP status 201.

### **UserLoginApi Class** (Handles user login):

- **`post()` method**:
  - Accepts email and password as input.
  - Verifies that both email and password are provided.
  - Checks if the user exists and validates the password using `Flask-Bcrypt`.
  - If successful, creates a JWT access token using `create_access_token` from `flask_jwt_extended`,
    and stores the user's details in the session.
  - Returns a success message with user data and the JWT token.
  - If authentication fails, returns a 404 error with an appropriate message.

### **UserEditApi Class** (Handles updating and deleting user profiles):

- **`put()` method**:
  - Accepts user data (email, username, and password) for updating the user's profile.
  - If no password is provided, it keeps the existing password; otherwise, it hashes the new password.
  - Attempts to update the user's data in the database using `UserModel.update()`.
  - If the update is successful, it stores the updated user data in the session and returns a success message.
  - If an error occurs, returns a 404 error message.

- **`delete()` method**:
  - Deletes the user with the specified `id` from the database using `UserModel.find_and_delete_by_id()`.
  - Returns a success message if the user is deleted successfully; otherwise, returns an error message.

### **UserForgotPassword Class** (Handles password reset request):

- **`post()` method**:
  - Accepts an `email` as input and checks if the user exists using `UserModel.find_by_email()`.
  - If the user exists, generates a password reset token using `URLSafeTimedSerializer`.
  - Sends a password reset link via email using `Flask-Mail`. The email contains a link for resetting the password.
  - Returns a success message after sending the email.

### **UserResetPassword Class** (Handles resetting the user's password):

- **`put()` method**:
  - Accepts a new `password` as input and hashes it using `Flask-Bcrypt`.
  - Updates the user's password in the database using `UserModel.update()`.
  - If the update is successful, stores the updated user data in the session and returns a success message.
  - If an error occurs, returns a 404 error message.

### **Key Features**:
- **User Registration and Login**: Handles user sign-up, login with password verification, and session management.
- **Email Verification**: Sends email verification links to users during registration.
- **Password Reset**: Allows users to request a password reset link via email and update their password securely.
- **JWT Authentication**: Implements JWT-based authentication to secure user logins.
- **Profile Management**: Allows users to update their profile and delete their account.
- **Flask-Mail Integration**: Uses Flask-Mail to send emails for registration, verification, and password reset processes.
- **Session Management**: Stores user data and a list of users in the session for session-based state management.

In summary, this code implements a set of RESTful API endpoints to manage user registration, 
login, profile editing, email verification, and password reset using Flask, Flask-RESTful, Flask-JWT-Extended,
and Flask-Mail. It also includes security features such as password hashing, JWT tokens, and
email-based password recovery.'''

from flask_restful import Resource
from flask import request, session, url_for
from database.userModel import UserModel
from flask_jwt_extended import create_access_token
from extension import bcrypt
from flask import url_for
from extension import mail
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
 

s = URLSafeTimedSerializer('ExpErtsystEmsOlUtIOn') 


class UserVerifyApi(Resource):
    def post(self, email):
        
        # Check if the user already exists :
        if UserModel.find_by_email(email):
            return {'message': ' This email already exists'}, 200
        
        # Email verification : 
        token = s.dumps(email, salt='email-confirmation')
        msg = Message('Email Verification', sender='cozykme@gmail.com', recipients=[email])
        link = url_for("register", token=token, _external=True)
        msg.body = f'Verify your email by clicking on this link: {link}'
        mail.send(msg) 
        
        return {'message': 'Success'}, 200 
 
class UserApi(Resource):
    def get(self):
        users = UserModel.find_all()
        session['user_list'] = [user.to_dict() for user in users] 
        return {'users': [user.to_dict() for user in users]}, 200
  
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        username = data.get('username')
        role = data.get('role')
               
        # Validate input data
        if not email or not password or not username or not role:
            return {'message': 'Missing required fields'}, 200 
        
        # Decoding Hash password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Create and save the new user
        new_user = UserModel(email=email, password=hashed_password, username=username, role=role)
        new_user.save()
        
        return {'message': 'Success'}, 201
    
class UserLoginApi(Resource):
    
    def post(self):
        data = request.get_json()
         
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return {'message': 'Missing required fields'}, 200

        user = UserModel.find_by_email(email)
        if user and bcrypt.check_password_hash(user.password, password):
            # Session & Token
            token = create_access_token(identity=user.id)
            session['user'] = user.to_dict()
            users = UserModel.find_all()
            session['user_list'] = [user.to_dict() for user in users]
            return {'message': 'Success', 'user': user.to_dict(), 'token': token}, 200        
        
        return {'message': 'Kindly check your email or password again!'}, 404

class UserEditApi(Resource):
    def put(self, id):
        data = request.get_json()
        
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        
        if not email or not username or not id:
            return {'message': 'Missing required fields'}, 400    
        
        # if password not available, replace it with the old password
        if not password:
            user = UserModel.find_by_id(id)
            if not user:
                return {'message': 'User not found'}, 404
            hashed_password = user.password  
        else:    
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # create object and save the updated data    
        update_data = {'email': email, 'password': hashed_password, 'username': username}
        updated_user = UserModel.update(id, update_data)
       
        if updated_user:
            session['user'] = updated_user.to_dict()
            return {'message': 'Success', 'user': updated_user.to_dict()}, 200
        
        return {'message': 'Some Error during updating your profile, please try later!'}, 404
    
    def delete(self, id):
        deleted_user = UserModel.find_and_delete_by_id(id)
        if deleted_user is None:
            return {'message': 'Success'}, 200
        return {'message': "There is some error in deleting your account"}, 404

class UserForgotPassword(Resource):
    def post(self, email):
        
        user = UserModel.find_by_email(email)
        if not user:
            return {'message': ' This email does not exists'}, 200
        
        token = s.dumps(user.id, salt='password-forgot')
        msg = Message('Reset Password Link', sender='cozykme@gmail.com', recipients=[email])
        link = url_for("resetpassword", token=token, _external=True)
        msg.body = f'Reset your password by clicking on this link: {link}'
        mail.send(msg) 
        
        return {'message': 'Success'}, 200        
    
class UserResetPassword(Resource):
    def put(self, id):
        data = request.get_json()
        
        password = data.get('password')
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # create object and save the updated data    
        update_data = {'password': hashed_password}
        updated_user = UserModel.update(id, update_data)
       
        if updated_user:
            session['user'] = updated_user.to_dict()
            return {'message': 'Success', 'user': updated_user.to_dict()}, 200
        
        return {'message': 'Some Error during updating your profile, please try later!'}, 404   