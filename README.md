# CS504_groupproject

bring the container up with:
    sudo docker-compose up -d --build
close container with this command:
    
    cleans generated files


db: CS_504_PROJECT
table users: CREATE TABLE users (
            id int NOT NULL PRIMARY KEY,
            username varchar(255) NOT NULL,
            email varchar(255),
            password varchar(255),
            telephone varchar(255)
            );

insert data:insert into users(id, username, email, password, telephone)
            values(1, "John", 'john@zyx.com', '1234', '999-345-8987');
            insert into users(id, username, email, password, telephone)
            values(2, "Tom", 'topm@zyx.com', '1234', '920-309-3344');
            insert into users(id, username, email, password, telephone)
            values(3, "Edna", 'edna@zyx.com', '1234', '859-321-9009');
            insert into users(id, username, email, password, telephone)
            values(4, "Mike", 'mike@zyx.com', '1234', '409-435-9904');
            insert into users(id, username, email, password, telephone)
            values(5, "Jill", 'jill@zyx.com', '1234', '415-453-8099');