""" 
    Title: whatabook_master.py
    Author: Ebenezer Evanoff
    Date: 02 December 2023
    Description: Program to add books, users, and wishlist items to the whatabook database
"""

""" import statements """
import argparse
import mysql.connector
from mysql.connector import errorcode

""" argument parser configuration """
parser = argparse.ArgumentParser()
parser.add_argument("--add_user", help="Add a user to the database", action="store_true")
parser.add_argument("--first_name", help="The user's first name")
parser.add_argument("--last_name", help="The user's last name")
parser.add_argument("--user_id", help="The user's ID number")
parser.add_argument("--book_name", help="The book's name")
parser.add_argument("--book_author", help="The book's author")
parser.add_argument("--book_id", help="The book's ID number")
parser.add_argument("--store_id", help="The store's ID number")
parser.add_argument("--file", help="The file to read from")
parser.add_argument("--add_wishlist", help="Add a book to a user's wishlist", action="store_true")
parser.add_argument("--show_books", help="Show all books in the database", action="store_true")
parser.add_argument("--show_users", help="Show all users in the database", action="store_true")
parser.add_argument("--show_wishlist", help="Show all wishlist items for user", action="store_true")
args = parser.parse_args()

""" global variables """
add_user = args.add_user
first_name = args.first_name
last_name = args.last_name
user_id = args.user_id
book_name = args.book_name
book_author = args.book_author
book_id = args.book_id
store_id = args.store_id
file = args.file
add_wishlist = args.add_wishlist
show_books = args.show_books
show_users = args.show_users
show_wishlist = args.show_wishlist

""" database config object """
config = {
    "user": "whatabook_user",
    "password": "MySQL8IsGreat!",
    "host": "127.0.0.1",
    "database": "whatabook",
    "raise_on_warnings": True
}

try:
    """ Connect to the whatabook database """ 

    # connect to the whatabook database
    db = mysql.connector.connect(**config)  

    # get the cursor object
    cursor = db.cursor()


    """ read file and add books to database """
    if file:

        with open (file, "r") as books:
            for line in books:
                line = line.strip().split(",")
                book_name, book_author, details = line[0], line[1], line[2]
                if not details.strip():
                    details = None
                cursor.execute("INSERT INTO book (book_name, author, details) VALUES ('{}', '{}', '{}')".format(book_name, book_author, details))
                db.commit()
                print("ADDING Book Name: {}\n Author: {}\n Details: {}\n\n".format(book_name, book_author, details))
        print("-- All Books added successfully --\n\n")

    """ add a new user to the database """
    if add_user and first_name and last_name:
        cursor.execute("INSERT INTO user (first_name, last_name) VALUES ('{}', '{}')".format(first_name, last_name))
        db.commit()
        print("ADDING User: {} {}\n\n".format(first_name, last_name))

    """ add a book to a user's wishlist """
    if add_wishlist and book_id and user_id:
        cursor.execute("INSERT INTO wishlist (user_id, book_id) VALUES ('{}', '{}')".format(user_id, book_id))
        db.commit()
        print("ADDING Book ID: {}\n To User ID: {}\n\n".format(book_id, user_id))

    """ show all books in the database """
    if show_books:
        cursor.execute("SELECT book_id, book_name, author, details FROM book")
        books = cursor.fetchall()
        print("\n -- DISPLAYING BOOKS --")
        for book in books:
            print(" Book ID: {}\n Book Name: {}\n Author: {}\n Details: {}\n".format(book[0], book[1], book[2], book[3]))

    """ show all users in the database """
    if show_users:
        cursor.execute("SELECT user_id, first_name, last_name FROM user")
        users = cursor.fetchall()
        print("\n -- DISPLAYING USERS --")
        for user in users:
            print(" User ID: {}\n First Name: {}\n Last Name: {}\n".format(user[0], user[1], user[2]))

    """ show all wishlist items for user """
    if show_wishlist and user_id:
        cursor.execute("SELECT user.user_id, user.first_name, user.last_name, book.book_id, book.book_name, book.author FROM user " 
                       "INNER JOIN wishlist ON wishlist.user_id = user.user_id INNER JOIN book ON wishlist.book_id = book.book_id WHERE user.user_id = {}".format(user_id))
        wishlist = cursor.fetchall()
        print("\n -- DISPLAYING WISHLIST ITEMS --")
        for item in wishlist:
            print(" User ID: {}\n First Name: {}\n Last Name: {}\n Book ID: {}\n Book Name: {}\n Author: {}\n".format(item[0], item[1], item[2], item[3], item[4], item[5]))

except mysql.connector.Error as err:

    """ handle errors """ 
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print(" The supplied username or password are invalid")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print(" The specified database does not exist")

    else:
        print(err)

finally:
    """ close the connection to MySQL """
    db.close()