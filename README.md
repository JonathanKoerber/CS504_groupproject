
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
|@users.route('/login', methods=['GET']) |  |
| @users.route('/login_mfa', methods=['GET'])| |
| @users.route('/users', methods=['POST']) | |
| @users.route('/users/', methods=['PUT']) | |
| @users.route('/users/', methods=['DELETE']) | |

#### ***mysql_db***


#### ***adminer***
