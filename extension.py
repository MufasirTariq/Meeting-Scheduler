'''This code snippet initializes two important extensions for a Flask web application:

1. **Bcrypt**: 
   - **`Bcrypt`** is a password hashing library that provides a secure way to hash and verify passwords in 
    Flask applications. By initializing `bcrypt = Bcrypt()`, you're setting up the extension to handle 
    password hashing securely. It is typically used to hash user passwords before storing them in a database and
    to check passwords during user authentication.

2. **Mail**: 
   - **`Mail`** is an extension that integrates email functionality into a Flask application. 
    By initializing `mail = Mail()`, this object can be used to send emails, such as for user 
    registration verification, password resets, or general notifications. It requires email configuration settings
    (e.g., SMTP server) to work effectively.

In summary, this code sets up the infrastructure to handle secure password management (via Bcrypt) and 
email functionalities (via Mail) within a Flask application.'''

from flask_bcrypt import Bcrypt
from flask_mail import Mail

bcrypt = Bcrypt()
mail = Mail()