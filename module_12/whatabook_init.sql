/*
    Title: whatabook_init.sql
    Author: Ebenezer Evanoff
    Date: 12/11/2023
    Description: Whatabook database initialization script.
*/

-- delete whatabook database if it exists
DROP DATABASE IF EXISTS whatabook;

-- drop test user if exists
DROP USER IF EXISTS 'whatabook_user'@'localhost';

-- create whatabook database
CREATE DATABASE whatabook;

-- create whatabook_user and grant them all privileges to the whatabook database
CREATE USER 'whatabook_user'@'localhost' IDENTIFIED BY 'MySQL8IsGreat!';

-- grant all privileges to the whatabook database to user whatabook_user on localhost
GRANT ALL PRIVILEGES ON whatabook.* TO 'whatabook_user'@'localhost';

-- flush privileges
FLUSH PRIVILEGES;

-- use whatabook database
USE whatabook;

-- create store table
CREATE TABLE store (
    store_id INT NOT NULL AUTO_INCREMENT,
    locale VARCHAR(500) NOT NULL,
    PRIMARY KEY(store_id)
);

-- create book table
CREATE TABLE book (
    book_id INT NOT NULL AUTO_INCREMENT,
    book_name VARCHAR(200) NOT NULL,
    author VARCHAR(200) NOT NULL,
    details VARCHAR(500),
    PRIMARY KEY(book_id)
);

-- create user table
CREATE TABLE user (
    user_id INT NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(75) NOT NULL,
    last_name VARCHAR(75) NOT NULL,
    PRIMARY KEY(user_id)
);

-- create wishlist table
CREATE TABLE wishlist (
    wishlist_id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    book_id INT NOT NULL,
    PRIMARY KEY (wishlist_id),
    CONSTRAINT fk_book
    FOREIGN KEY (book_id)
        REFERENCES book(book_id),
    CONSTRAINT fk_user
    FOREIGN KEY (user_id)
        REFERENCES user(user_id)
);

-- insert store record (Trivia: This is the last Blockbuster store in the United States)
INSERT INTO store(locale) VALUES('211 NE Revere Ave, Bend, OR 97701');

-- insert book records
INSERT INTO book(book_name, author, details) VALUES('The Return of the King', 'J.R.Tolkien', 'The third part of The Lord of the Rings');
INSERT INTO book(book_name, author, details) VALUES('The Fellowship of the Ring', 'J.R.Tolkien', 'The first part of The Lord of the Rings');
INSERT INTO book(book_name, author, details) VALUES('The Two Towers', 'J.R.Tolkien', "The second part of The Lord of The Rings");
INSERT INTO book(book_name, author) VALUES('The Hobbit or There and Back Again', 'J.R.Tolkien');
INSERT INTO book(book_name, author) VALUES('Dune: Deluxe Edition', 'Frank Herbert');
INSERT INTO book(book_name, author) VALUES("Charlotee's Web", 'E.B. White');
INSERT INTO book(book_name, author) VALUES('The Great Gatsby', 'F. Scott Fitzgerald');
INSERT INTO book(book_name, author) VALUES('The Lion, the Witch, and the Wardrobe', 'C.S. Lewis');
INSERT INTO book(book_name, author) VALUES('The Catcher and the Rye', 'J.D. Salinger');
INSERT INTO book(book_name, author) VALUES('The Grapes of Wrath', 'John Steinbeck');
INSERT INTO book(book_name, author) VALUES('The Adventures of Huckleberry Finn', 'Mark Twain');
INSERT INTO book(book_name, author) VALUES('The Adventures of Tom Sawyer', 'Mark Twain');
INSERT INTO book(book_name, author, details) VALUES('To Kill a Mockingbird', 'Harper Lee', 'A classic of American literature');
INSERT INTO book(book_name, author, details) VALUES('In Search of Lost Time', 'Marcel Proust', 'A modernist novel');
INSERT INTO book(book_name, author) VALUES('Ulysses', 'James Joyce');
INSERT INTO book(book_name, author) VALUES('Moby Dick', 'Herman Melville');
INSERT INTO book(book_name, author) VALUES('The Odyssey', 'Homer');
INSERT INTO book(book_name, author, details) VALUES('War and Peace', 'Leo Tolstoy', "Events leading to Napoleons's invasion of Russia");
INSERT INTO book(book_name, author) VALUES('Hamlet', 'William Shakespeare');
INSERT INTO book(book_name, author) VALUES('Nineteen Eighty Four', 'George Orwell');
INSERT INTO book(book_name, author, details) VALUES("Alice's Adventures in Wonderland", 'Lewis Carroll', 'Down the rabbit hole');

-- insert user records
INSERT INTO user(first_name, last_name) VALUES('Thorin', 'Oakenshield');
INSERT INTO user(first_name, last_name) VALUES('Bilbo', 'Baggins');
INSERT INTO user(first_name, last_name) VALUES('Frodo', 'Baggins');
INSERT INTO user(first_name, last_name) VALUES('John', 'Cena');
INSERT INTO user(first_name, last_name) VALUES('Clint', 'Eastwood');
INSERT INTO user(first_name, last_name) VALUES('Dwayne', 'Johnson');
INSERT INTO user(first_name, last_name) VALUES('Samuel', 'Jackson');
INSERT INTO user(first_name, last_name) VALUES('Steve', 'Austin');
INSERT INTO user(first_name, last_name) VALUES('Randy', 'Savage');
INSERT INTO user(first_name, last_name) VALUES('Scarlett', 'Johansson');
INSERT INTO user(first_name, last_name) VALUES('Hulk', 'Hogan');
INSERT INTO user(first_name, last_name) VALUES('Robert', 'De Niro');
INSERT INTO user(first_name, last_name) VALUES('Ric', 'Flair');
INSERT INTO user(first_name, last_name) VALUES('Shawn', 'Michaels');
INSERT INTO user(first_name, last_name) VALUES('Brad', 'Pitt');
INSERT INTO user(first_name, last_name) VALUES('Angelina', 'Jolie');
INSERT INTO user(first_name, last_name) VALUES('Tom', 'Cruise');
INSERT INTO user(first_name, last_name) VALUES('Will', 'Smith');
INSERT INTO user(first_name, last_name) VALUES('Denzel', 'Washington');
INSERT INTO user(first_name, last_name) VALUES('Morgan', 'Freeman');
INSERT INTO user(first_name, last_name) VALUES('Al', 'Pacino');

-- insert wishlist records
INSERT INTO wishlist(user_id, book_id) VALUES((SELECT user_id FROM user WHERE first_name = 'Thorin' AND last_name = 'Oakenshield'), (SELECT book_id FROM book WHERE book_name = 'The Hobbit or There and Back Again'));
INSERT INTO wishlist(user_id, book_id) VALUES((SELECT user_id FROM user WHERE first_name = 'Bilbo' AND last_name = 'Baggins'), (SELECT book_id FROM book WHERE book_name = 'The Fellowship of the Ring'));
INSERT INTO wishlist(user_id, book_id) VALUES((SELECT user_id FROM user WHERE first_name = 'Frodo' AND last_name = 'Baggins'), (SELECT book_id FROM book WHERE book_name = 'The Return of the King'));
INSERT INTO wishlist(user_id, book_id) VALUES((SELECT user_id FROM user WHERE first_name = 'John' AND last_name = 'Cena'), (SELECT book_id FROM book WHERE book_name = 'The Two Towers'));
INSERT INTO wishlist(user_id, book_id) VALUES((SELECT user_id FROM user WHERE first_name = 'Dwayne' AND last_name = 'Johnson'), (SELECT book_id FROM book WHERE book_name = 'Dune: Deluxe Edition'));
INSERT INTO wishlist(user_id, book_id) VALUES((SELECT user_id FROM user WHERE first_name = 'Clint' AND last_name = 'Eastwood'), (SELECT book_id FROM book WHERE book_name = 'The Great Gatsby'));
INSERT INTO wishlist(user_id, book_id) VALUES((SELECT user_id FROM user WHERE first_name = 'Samuel' AND last_name = 'Jackson'), (SELECT book_id FROM book WHERE book_name = 'The Lion, the Witch, and the Wardrobe'));
INSERT INTO wishlist(user_id, book_id) VALUES((SELECT user_id FROM user WHERE first_name = 'Steve' AND last_name = 'Austin'), (SELECT book_id FROM book WHERE book_name = 'The Catcher and the Rye'));
INSERT INTO wishlist(user_id, book_id) VALUES((SELECT user_id FROM user WHERE first_name = 'Randy' AND last_name = 'Savage'), (SELECT book_id FROM book WHERE book_name = 'The Grapes of Wrath'));
INSERT INTO wishlist(user_id, book_id) VALUES((SELECT user_id FROM user WHERE first_name = 'Scarlett' AND last_name = 'Johansson'), (SELECT book_id FROM book WHERE book_name = 'The Adventures of Huckleberry Finn'));
INSERT INTO wishlist(user_id, book_id) VALUES((SELECT user_id FROM user WHERE first_name = 'Hulk' AND last_name = 'Hogan'), (SELECT book_id FROM book WHERE book_name = 'The Odyssey'));