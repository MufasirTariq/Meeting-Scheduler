'''Here's a summary of what the provided code does:

- **Imports**:
  - `ObjectId` from `bson`: Used to handle MongoDB ObjectIds.
  - `mongo` from `database.db`: The PyMongo instance for interacting with MongoDB.
  - `UserModel` from `database.userModel`: A model for interacting with the User data.

- **MeetingModel Class**:
  - Represents a meeting in the system with attributes like `user_id`, `url`, `platform`, `time`, `date`, `msg`, and `meeting_id`.

- **Constructor (`__init__`)**:
  - Initializes a new instance of `MeetingModel` with the specified attributes (`user_id`, `url`, `platform`, `time`, `date`, `msg`, `meeting_id`).

- **`save()` method**:
  - Saves the meeting data to the MongoDB collection `meeting`.
  - Inserts the meeting data and updates the model instance with the generated `meeting_id`.

- **`find_all()` method**:
  - Retrieves all meetings from the `meeting` collection.
  - Returns a list of `MeetingModel` instances for each document in the collection.

- **`find_by_user_id()` method**:
  - Searches for a meeting based on the `user_id`.
  - Returns a `MeetingModel` instance for the first meeting found or `None` if no meeting exists.

- **`to_dict()` method**:
  - Converts the `MeetingModel` instance into a dictionary format for easier manipulation or JSON serialization.
  
- **`find_by_id_and_delete()` method**:
  - Finds a meeting by its `meeting_id` and deletes it from the database.
  - Returns a success message or an error message if no meeting is found.

- **`find_by_id()` method**:
  - Finds a meeting by its `meeting_id`.
  - Returns a `MeetingModel` instance for the meeting if found, or `None` if not found.

- **`find_by_date()` method**:
  - Finds a meeting by its `date` attribute.
  - Returns a `MeetingModel` instance for the meeting if found, or `None` if not found.

- **`populate_user()` method**:
  - Retrieves the user data associated with the `user_id` from the `UserModel`.
  - If the user is found, it stores the user data in the `user_data` attribute of the `MeetingModel` instance.

In summary, this code provides functionality for managing meetings in a MongoDB database, including creating, 
retrieving, updating, deleting, and linking meetings with associated user data.'''

from bson import ObjectId 
from database.db import mongo
from database.userModel import UserModel
 
class MeetingModel:
    def __init__(self, user_id, url, platform, time, date, msg=None, meeting_id=None):
        self.id = meeting_id  
        self.user_id = user_id
        self.url = url
        self.platform = platform
        self.time = time
        self.date = date
        self.msg = msg

    def save(self):
        meeting_data = { 'user_id': self.user_id,'url': self.url,'platform': self.platform,
            'time': self.time,'date': self.date,'msg': self.msg
        }
        
        result = mongo.db.meeting.insert_one(meeting_data)  
        self.id = str(result.inserted_id)  

    @staticmethod
    def find_all():
        meetings = mongo.db.meeting.find()
        return [MeetingModel(m['user_id'], m['url'], m['platform'], m['time'], m['date'], m['msg'],
                             str(m['_id'])) for m in meetings]

    @staticmethod
    def find_by_user_id(user_id):
        meeting_data = mongo.db.meeting.find_one({'user_id': user_id})
        if meeting_data:
            return MeetingModel(meeting_data['user_id'], meeting_data['url'], meeting_data['platform'], 
                                meeting_data['time'], meeting_data['date'], meeting_data['msg'],
                                str(meeting_data['_id']))
        return None

    def to_dict(self):
        return {
            'user_id': self.user_id,'url': self.url,'platform': self.platform,
            'time': self.time,'date': self.date,'msg': self.msg,'id': self.id
        }
        
    @staticmethod
    def find_by_id_and_delete(meeting_id):
        meeting_data = mongo.db.meeting.find_one({'_id': ObjectId(meeting_id)})
        if meeting_data:
            mongo.db.meeting.delete_one({'_id': ObjectId(meeting_id)})
            return None    
        return {'message': 'Meeting not found'}
        
    @staticmethod
    def find_by_id(meeting_id):
        meeting_data = mongo.db.meeting.find_one({'_id': ObjectId(meeting_id)})
        if meeting_data:
            return MeetingModel(
                user_id=meeting_data['user_id'],
                url=meeting_data['url'],
                platform=meeting_data['platform'],
                time=meeting_data['time'],
                date=meeting_data['date'],
                msg=meeting_data['msg'],
                meeting_id=str(meeting_data['_id'])
            )
        return None
        
    @staticmethod
    def find_by_date(date):
        meeting_data = mongo.db.meeting.find_one({'date': date})
        if meeting_data:
            return MeetingModel(
                user_id=meeting_data['user_id'],
                url=meeting_data['url'],
                platform=meeting_data['platform'],
                time=meeting_data['time'],
                date=meeting_data['date'],
                msg=meeting_data['msg'],
                meeting_id=str(meeting_data['_id']),
                
            )
        return None    
        
    def populate_user(self):
        user = UserModel.find_by_id(self.user_id)
        if user:
            self.user_data = user.to_dict()  
        else:
            self.user_data = None    