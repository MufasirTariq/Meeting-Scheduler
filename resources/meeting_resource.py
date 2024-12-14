'''Here's a summary of what the provided code does:

- **Imports**:
  - `Resource` from `flask_restful`: Used to create API resources.
  - `request` and `url_for` from `flask`: For handling HTTP requests and generating URLs.
  - `MeetingModel` and `UserModel` from `database.meetingModel` and `database.userModel`: 
     Used for interacting with MongoDB collections for meetings and users.
  - `mail` from `extension`: Configured instance for sending emails using Flask-Mail.
  - `Message` from `flask_mail`: To create email messages.
  - `URLSafeTimedSerializer` from `itsdangerous`: For generating and validating timed tokens 
    (though not used in this specific code).

### **MeetingApi Class** (Handles API operations related to meetings):

- **`get()` method**:
  - Retrieves all meetings from the database using `MeetingModel.find_all()`.
  - For each meeting, it fetches the associated user details (e.g., `username`) using `UserModel.find_by_id()`.
  - Returns a list of meeting details along with the user's username in the response.

- **`post()` method**:
  - Accepts JSON input data from the client, containing information about the meeting 
    (e.g., `username`, `platform`, `time`, `date`, `url`, `msg`).
  - Validates that all required fields are provided. If any are missing, returns an error response.
  - Creates a new `MeetingModel` instance with the provided data and saves it to the database.
  - After saving the meeting, retrieves the user's email and username.
  - Sends a confirmation email to the user using `Flask-Mail`, which contains a professionally 
    designed HTML template with meeting details (e.g., date, time, platform, message).
  - Returns a success response with the newly created meeting data.

### **MeetingEditApi Class** (Handles editing and deletion of meetings):

- **`delete()` method**:
  - Accepts a `meeting_id` (passed as `id` in the URL) and attempts to find and delete the meeting 
    from the database using `MeetingModel.find_by_id_and_delete()`.
  - If the meeting is successfully deleted, returns a success message with a 200 status code.
  - If the meeting is not found or not deleted, returns a 404 error with a corresponding message.

### **Key Features**:
- **CRUD Operations for Meetings**: The code provides functionality to create, retrieve, and delete meetings.
- **User Interaction**: The meeting API retrieves user details associated with each 
    meeting and sends confirmation emails using Flask-Mail.
- **Email Confirmation**: After creating a meeting, an email with HTML content is sent to the user, 
    confirming meeting details.
- **Error Handling**: Checks for missing or invalid input data, and returns appropriate error messages 
    when required fields are not provided or when meetings cannot be found or deleted.

In summary, this code implements API endpoints to manage meetings and send email notifications using Flask,
including features for creating, listing, and deleting meetings, as well as handling user data and 
sending confirmation emails.'''

from flask_restful import Resource
from flask import request, url_for
from database.meetingModel import MeetingModel
from database.userModel import UserModel
from extension import mail
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer

s = URLSafeTimedSerializer('ExpErtsystEmsOlUtIOn') 

class MeetingApi(Resource):
    def get(self):
        meetings = [] 
        meeting_list = MeetingModel.find_all()
        for meeting in meeting_list:
            m = meeting.to_dict()
            user = UserModel.find_by_id(m['user_id'])
            if user:  # Check if user exists
                meet = {
                    'username': user.to_dict()['username'],'user_id': m['user_id'], 'url': m['url'],
                    'platform': m['platform'],'time': m['time'],'date': m['date'],
                    'msg': m['msg'],'id': m['id']
                }
                meetings.append(meet)
        return {'meetings': meetings}, 200
    
    def post(self):
        data = request.get_json() 
        if not data:
            return {'message': 'No input data provided'}, 400

        user_id = data.get('username') 
        platform = data.get('platform')
        time = data.get('time')
        date = data.get('date')
        url = data.get('url')
        msg = data.get('msg')

        # Validate input data
        if not user_id or not platform or not time or not date or not url:
            return {'message': 'Missing required fields'}, 400

        meet = MeetingModel(user_id=user_id, url=url, platform=platform, time=time, date=date, msg=msg)
        meet.save()
        
        user = UserModel.find_by_id(user_id)
        user = user.to_dict()
        email = user['email'] 
        username = user['username'] 
        print(msg)
        
        # mail confirmation
        mail_msg = Message('Meeting Details', sender='cozykme@gmail.com', recipients=[email])
        
        # Create a more professional HTML email body
        mail_msg.html = f"""\
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Meeting Details</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    margin: 0;
                    padding: 0;
                    background-color: #f9f9f9;
                }}
                .container {{
                    max-width: 600px;
                    margin: 20px auto;
                    background-color: #ffffff;
                    border-radius: 5px;
                    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                    padding: 20px;
                }}
                .header {{
                    background-color: #c0392b; /* Red color */
                    color: #ffffff;
                    padding: 10px 20px;
                    text-align: center;
                    border-radius: 5px 5px 0 0;
                }}
                h2 {{
                    color: #333;
                    margin: 0;
                }}
                p {{
                    color: #555;
                }}
                ul {{
                    list-style-type: none;
                    padding: 0;
                }}
                li {{
                    margin: 10px 0;
                }}
                a {{
                    color: #c0392b; /* Red color for links */
                    text-decoration: none;
                }}
                a:hover {{
                    text-decoration: underline;
                }}
                .footer {{
                    margin-top: 10px;
                    font-size: 0.9em;
                    color: #777;
                    text-align: center;
                    padding: 10px 0;
                    background-color: #f2f2f2;
                    border-top: 1px solid #e0e0e0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>Meeting Details</h2>
                </div>
                <p>Dear {username},</p>
                <p>I hope this message finds you well.</p>
                <p>Please find the details for the upcoming meeting below:</p>
                <ul>
                    <li><strong>Date:</strong> {date}</li>
                    <li><strong>Time:</strong> {time}</li>
                    <li><strong>Platform:</strong> {platform}</li>
                    <li><strong>Meeting URL:</strong> <a href="{url}">{url}</a></li>
                    <li><strong>Message:</strong> {msg}</li>
                </ul>
                <p>Should you have any questions or need further assistance, please do not hesitate to reach out.</p>
                <p>Looking forward to our meeting.</p>
                <p>Best regards,</p>
                <p>Expert System Solution</p>
                <p>Contact : +92 301 1234567</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        mail.send(mail_msg)  
        
        return {'message': 'Success', 'meeting': meet.to_dict()}, 201
        
class MeetingEditApi(Resource):
    def delete(self, id):
        deleted_meeting = MeetingModel.find_by_id_and_delete(id)
        if deleted_meeting is None: 
            return {'message': 'Success'}, 200      
        return {'message': "Meeting not found or not deleted"}, 404
    