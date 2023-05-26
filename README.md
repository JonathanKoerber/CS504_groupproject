
# Flask API Project for CS_504 

## Software Engeineering 

This project is the coding portion of the final project for the course. It is a REST API authentication service. The backend is written in Python using the Flask framework, using a MySQL database that Adminer administers. 

### Starting app

```docker-compose up --build -d```

###  Containers 
______________
 
#### *flask_api*:
This is the flask instance.
Runs at [127.0.0.1:5000](http://127.0.0.1:5000). Takes HTTP request on the following roots all params neet to be added to the body of he request. 

#### ***Routes***
| Route | Descripiton   |
| -------------- | ------------------------|
| @users.route('/')| This route is just for debug it return all users in the. Created to make the aid the development process.         | 
|@users.route('/login', methods=['GET']) | User login. Accepts a request body with `{ username: "<>" , password: "<>", and mfa: "sms"}` |
| @users.route('/login_mfa', methods=['GET'])| MFA login. Accepts a request body with `{ username: "<>" , pin: "<>"}`|
| @users.route('/users', methods=['POST']) | Creates new user|
| @users.route('/users/', methods=['PUT']) | Updates user|
| @users.route('/users/', methods=['DELETE']) | Deletes user|

#### ***mysql_db***
A instance of MySQL database. Data from the app persists in the volume `/storage`. If for some reason you want to rebuild the container the `/storage` directry will need to be deleted. This shouldn't need to happen. 


#### ***adminer***
Adminer is availible at [127.0.0.1:8080](http://127.0.0.1:8080). To login select `mysql_db` and enter `username: root password: root`. Its not a greate idea to add data here because fask_api app is expecting passwords to be hashed. 

**TODO** Add python or pash script that will add users to database using the sqlalchemy db object. 

#### ***Envirment File***
To run the applciaiton you'll need to create a file named `.env` in the projects root directry. A template for the file is below. To have valid multifactor authentication work you need to create an sms channel acount with [Twilo](https://www.twilio.com) and add the tokens to the `.env` file. 

```
DATABASE_URL = 'mysql+mysqlconnector://root:root@localhost:3306/CS_504_PROJECT'
TWILIO_ACCOUNT_SID=''
TWILIO_AUTH_TOKEN=''
TWILIO_VERIFY_SERVICE_ID=
EMAIL_ACC = ''
MAIL_PASSWORD = ''
PHONE_NUMBER = ''
```