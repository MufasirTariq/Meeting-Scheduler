'''Here's a summary of what the provided code does:

- **Imports**:
  - `ObjectId` from `bson.objectid`: Used to handle MongoDB ObjectIds.
  - `mongo` from `database.db`: The PyMongo instance for interacting with MongoDB.

- **UserModel Class**:
  - Represents a user in the system with attributes like `email`, `password`, `username`, `role`, and `user_id`.

- **Constructor (`__init__`)**:
  - Initializes a new instance of `UserModel` with the specified attributes (`email`, `password`, `username`, `role`, `user_id`).

- **`save()` method**:
  - Saves the user data to the MongoDB `users` collection.
  - Inserts the user data and updates the model instance with the generated `user_id`.

- **`find_all()` method**:
  - Retrieves all users from the `users` collection.
  - Returns a list of `UserModel` instances for each document in the collection.

- **`find_by_email()` method**:
  - Searches for a user based on the `email`.
  - Returns a `UserModel` instance for the first user found, or `None` if no user exists with that email.

- **`find_by_id()` method**:
  - Searches for a user by their `user_id` (MongoDB ObjectId).
  - Returns a `UserModel` instance for the user if found, or `None` if no user is found.

- **`find_and_delete_by_id()` method**:
  - Finds a user by their `user_id` and deletes the user from the database.
  - Returns a success message or an error message if no user is found.

- **`to_dict()` method**:
  - Converts the `UserModel` instance into a dictionary format for easier manipulation or JSON serialization.

- **`update()` method**:
  - Updates a user's information in the `users` collection using the provided `update_data`.
  - Returns the updated `UserModel` instance if the update is successful, or `None` if no changes were made.

In summary, this code defines the `UserModel` class, which provides functionality for managing user 
data in a MongoDB database. It includes methods for creating, retrieving, updating, deleting, 
and converting user data into dictionaries.'''

from bson.objectid import ObjectId
from database.db import mongo
 
class UserModel:
    def __init__(self, email, password, username, role, user_id=None):
        self.id = user_id  
        self.email = email
        self.password = password
        self.username = username
        self.role = role

    def save(self):
        user_data = {
            'email': self.email,
            'password': self.password,
            'username': self.username,
            'role': self.role,
        }
        result = mongo.db.users.insert_one(user_data)  
        self.id = str(result.inserted_id)  

    @staticmethod
    def find_all():
        users = mongo.db.users.find()
        return [UserModel(user['email'], user['password'], user['username'], user['role'], str(user['_id'])) for user in users]

    @staticmethod
    def find_by_email(email):
        user_data = mongo.db.users.find_one({'email': email})
        if user_data:
            return UserModel(user_data['email'], user_data['password'], user_data['username'], user_data['role'], str(user_data['_id']))
        return None
    
    @staticmethod
    def find_by_id(user_id):
        user_data = mongo.db.users.find_one({'_id': ObjectId(user_id)})
        if user_data:
            return UserModel(user_data['email'], user_data['password'], user_data['username'], user_data['role'], str(user_data['_id']))
        return None

    @staticmethod
    def find_and_delete_by_id(user_id):
        user_data = mongo.db.users.find_one({'_id': ObjectId(user_id)})
        if user_data:
            mongo.db.users.delete_one({'_id': ObjectId(user_id)})
            return None
        
        return {'message': 'User  not found'}

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'role': self.role
        }
    
    @staticmethod
    def update(user_id, update_data):
        if not ObjectId.is_valid(user_id):
            return None
        
        result = mongo.db.users.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': update_data}
        )
        
        if result.modified_count > 0:
            updated_user_data = mongo.db.users.find_one({'_id': ObjectId(user_id)})
            if updated_user_data:
                return UserModel(
                    updated_user_data['email'],
                    updated_user_data['password'],
                    updated_user_data['username'],
                    updated_user_data['role'],
                    str(updated_user_data['_id'])
                )
        return None