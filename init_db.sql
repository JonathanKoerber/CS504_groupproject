create DATABASE IF NOT EXISTS `CS_504_PROJECT`;

CREATE TABLE IF NOT EXISTS users (
            id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
            username varchar(255) NOT NULL,
            email varchar(255),
            password varchar(255)
            );

insert into users(id, username, email, password)
            values(1, "John", 'john@zyx.com', '1234');
insert into users(id, username, email, password)
            values(2, "Tom", 'topm@zyx.com', '1234');
insert into users(id, username, email, password)
            values(3, "Edna", 'edna@zyx.com', '1234');
insert into users(id, username, email, password)
            values(4, "Mike", 'mike@zyx.com', '1234');
insert into users(id, username, email, password)
            values(5, "Jill", 'jill@zyx.com', '1234');