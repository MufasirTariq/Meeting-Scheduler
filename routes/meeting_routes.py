'''Here's a summary of what this code does:

### **Purpose**:
- This code sets up API routes for meeting-related operations in a Flask application using **Flask-RESTful**.

### **Function: `initialize_meeting_routes(app)`**:
- **Creates an API instance**:
  - `api = Api(app, prefix='/api/meeting')`: Initializes a Flask-RESTful `Api` object for the Flask app, 
    setting the base URL prefix for all meeting-related routes to `/api/meeting`.
  
- **Adds Resources (Routes)**:
  - `api.add_resource(MeetingApi, '/')`: Maps the `MeetingApi` class to the root endpoint (`/api/meeting/`).
    This class handles operations related to listing and creating meetings (GET and POST).
    
  - `api.add_resource(MeetingEditApi, '/<id>')`: Maps the `MeetingEditApi` class to the endpoint
    `/api/meeting/<id>`, where `<id>` is a dynamic parameter representing the meeting ID. 
    This class handles operations like editing and deleting meetings (PUT and DELETE).

### **Summary**:
This function sets up routes for managing meetings, with the following endpoints:
- **GET /api/meeting/**: Lists all meetings.
- **POST /api/meeting/**: Creates a new meeting.
- **PUT /api/meeting/<id>**: Updates a specific meeting by ID.
- **DELETE /api/meeting/<id>**: Deletes a specific meeting by ID.

In essence, this code establishes a clean and organized API for managing meetings in a Flask application.'''

from flask_restful import Api
from resources.meeting_resource import MeetingApi,MeetingEditApi

def initialize_meeting_routes(app):
    api = Api(app, prefix='/api/meeting')
    api.add_resource(MeetingApi, '/')
    api.add_resource(MeetingEditApi, '/<id>')