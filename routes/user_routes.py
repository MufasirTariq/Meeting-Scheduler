'''Here's a summary of what the provided code does:

### **Purpose**:
- This code sets up API routes for user-related operations in a Flask application using **Flask-RESTful**.

### **Function: `initialize_routes(app)`**:
- **Creates an API instance**:
  - `api = Api(app, prefix='/api')`: Initializes a Flask-RESTful `Api` object for the Flask app, with the base URL prefix set to `/api` for all user-related routes.

- **Adds Resources (Routes)**:
  - `api.add_resource(UserApi, '/user')`: Maps the `UserApi` class to the `/api/user` endpoint. This class handles user-related actions such as creating a user and listing all users (GET and POST).
  - `api.add_resource(UserEditApi, '/user/<id>')`: Maps the `UserEditApi` class to the `/api/user/<id>` endpoint, where `<id>` is a dynamic parameter representing the user ID. This class handles updating and deleting user profiles (PUT and DELETE).
  - `api.add_resource(UserLoginApi, '/login')`: Maps the `UserLoginApi` class to the `/api/login` endpoint, which handles user login (POST).
  - `api.add_resource(UserVerifyApi, '/useremailverify/<email>')`: Maps the `UserVerifyApi` class to the `/api/useremailverify/<email>` endpoint, where `<email>` is a dynamic parameter. This class handles email verification (POST).
  - `api.add_resource(UserForgotPassword, '/forgotpassword/<email>')`: Maps the `UserForgotPassword` class to the `/api/forgotpassword/<email>` endpoint. This class handles the password reset request process (POST).
  - `api.add_resource(UserResetPassword, '/resetpassword/<id>')`: Maps the `UserResetPassword` class to the `/api/resetpassword/<id>` endpoint, where `<id>` represents the user ID. This class handles the actual password reset process (PUT).

### **Summary**:
This function sets up user-related API routes, with the following endpoints:
- **POST /api/user**: Creates a new user.
- **GET /api/user**: Lists all users.
- **PUT /api/user/<id>**: Updates a user's profile by ID.
- **DELETE /api/user/<id>**: Deletes a user by ID.
- **POST /api/login**: Logs in a user and returns a JWT token.
- **POST /api/useremailverify/<email>**: Verifies the email address for registration.
- **POST /api/forgotpassword/<email>**: Initiates the password reset process by sending a reset link to the user's email.
- **PUT /api/resetpassword/<id>**: Resets a user's password by ID.

In essence, this code sets up all the necessary API routes for user management, including login,
registration, profile management, email verification, and password reset.'''

from flask_restful import Api
from resources.user_resource import UserApi, UserLoginApi, UserEditApi, UserVerifyApi, UserForgotPassword, UserResetPassword

def initialize_routes(app):
    api = Api(app, prefix='/api')
    api.add_resource(UserApi, '/user')
    api.add_resource(UserEditApi, '/user/<id>')
    api.add_resource(UserLoginApi, '/login')
    api.add_resource(UserVerifyApi, '/useremailverify/<email>')
    api.add_resource(UserForgotPassword, '/forgotpassword/<email>')
    api.add_resource(UserResetPassword, '/resetpassword/<id>')
    
      