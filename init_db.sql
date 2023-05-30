-- got to 127.0.1:8080
-- log in with username: root, password: root
-- select SQL command and run the following commands
-- This will delet all data in the database and create 
-- a new database with the following data

Drop DATABASE IF EXISTS `CS_504_PROJECT`;

create DATABASE IF NOT EXISTS `CS_504_PROJECT`;

use `CS_504_PROJECT`;

CREATE TABLE IF NOT EXISTS users (
            id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
            username varchar(255) NOT NULL UNIQUE,
            email varchar(255),
            phone_number varchar(20),
            password_hash varchar(255),
            otp_secret varchar(16)
            );

insert into users(id, username, email, phone_number, password_hash)
            values(1, "John", 'john@zyx.com', '1234567890', 'password');
insert into users(id, username, email, phone_number, password_hash)
            values(2, "Tom", 'topm@zyx.com', '1234567890','password');
insert into users(id, username, email, phone_number, password_hash)
            values(3, "Edna", 'edna@zyx.com', '1234567890', 'password');
insert into users(id, username, email, phone_number, password_hash)
            values(4, "Mike", 'mike@zyx.com', '1234567890','password');
insert into users(id, username, email, phone_number, password_hash)
            values(5, "Jill", 'jill@zyx.com', '1234567890','password');
        
select * from users;
