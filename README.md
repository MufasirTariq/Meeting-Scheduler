# Meeting Scheduler Application

**A web-based application for scheduling and managing meetings with advanced features such as user authentication, email verification, and an intuitive interface for both users and administrators.**

---

## **Features**

### **Core Functionalities**
- **User Panel**:
  - Schedule and manage meetings effortlessly.
  - Email and password validation with verification links sent via Gmail.
  - Secure login with token-based and session-based authentication.
- **Admin Dashboard**:
  - Manage users, meetings, and application settings from a centralized dashboard.
  - Monitor application activity with an intuitive interface.

### **Additional Features**
- **RESTful APIs**:
  - Integrated APIs for seamless data interaction and backend communication.
  - Built-in support for JSON-based data exchange.
- **AJAX and jQuery Integration**:
  - Enhanced user experience with dynamic, real-time updates.
  - Reduced page reloads for faster interaction.
- **Gmail API**:
  - Automated email notifications for user registration, password recovery, and meeting updates.

---

## **Technologies Used**

### **Frontend**
- **HTML**, **CSS**, **JavaScript**, **Bootstrap**
- **Jinja2 Templates** for dynamic content rendering

### **Backend**
- **Flask**: Lightweight and scalable web framework
- **Flask-RESTful**: For API development
- **Flask-JWT-Extended**: Secure token-based authentication
- **Flask-Mail**: Email handling
- **Flask-Bcrypt**: Password hashing

### **Database**
- **MongoDB**: NoSQL database for storing user and meeting data

### **Libraries and Tools**
- **AJAX & jQuery**: For dynamic and asynchronous web content
- **Python Libraries**:
  - Authentication: `bcrypt`, `Flask-JWT-Extended`
  - Email Handling: `email_validator`, `Flask-Mail`
  - API Development: `Flask-RESTful`
  - MongoDB Integration: `Flask-PyMongo`, `mongoengine`
- **Deployment**:
  - `gunicorn`, `waitress` for running the app

---

## **Setup Instructions**

Follow these steps to set up the Meeting Scheduler Application locally:

### **1. Clone the Repository**
```bash
git clone https://github.com/<your-username>/Meeting-Scheduler.git
cd Meeting-Scheduler
```

### **2. Create a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **3. Install Dependencies**
Install all required libraries listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```

### **4. Set Up Environment Variables**
Create a `.env` file in the root directory and include the following keys:
```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=<your-secret-key>
MONGO_URI=<your-mongo-database-uri>
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=<your-gmail-username>
MAIL_PASSWORD=<your-gmail-password>
```


## **Usage**

### **User Panel**
- Register, log in, and manage personal account settings.
- Schedule meetings with email notifications for updates.

### **Admin Dashboard**
- Access user and meeting management tools.
- View system logs and analytics.

---

## **Contribution Guidelines**

We welcome contributions to enhance the Meeting Scheduler Application. To contribute:
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes and commit them:
   ```bash
   git commit -m "Add your message here"
   ```
4. Push the changes to your forked repository:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Open a pull request.

---

## **License**

This project is licensed under the [MIT License](LICENSE).

---

## **Contact**

If you have any questions or suggestions, feel free to contact:
- **Name**: MUfasir Tariq
- **Email**: mufasirtariq@gmail.com
- **GitHub**: [Your GitHub Profile](https://github.com/MufasirTariq)

---

### **Acknowledgements**
- Flask Documentation: [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
- Bootstrap: [https://getbootstrap.com/](https://getbootstrap.com/)
- MongoDB: [https://www.mongodb.com/](https://www.mongodb.com/)

