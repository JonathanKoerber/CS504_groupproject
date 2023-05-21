# CS504_groupproject

bring the container up with:
    docker-compose up -d --build
close container with this command:
    docker-compose down -v


start the docker-compose containers
in browser go to 127.0.0.1:8080
sign in to mysql_db user: root password: root

select Select sql command and run:
create DATABASE IF NOT EXISTS `CS_504_PROJECT`;

select the CS_504_PROJECT then run: 
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

to check the db is working run:
select * from users