""" 
    Title: whatabook.py
    Author: Ebenezer Evanoff
    Date: 12/11/2023
    Description: WhatABook program; Console program that interfaces with a MySQL database
"""

""" import statements """
import sys
import mysql.connector
from mysql.connector import errorcode

""" database config object """
config = {
    "user": "whatabook_user",
    "password": "MySQL8IsGreat!",
    "host": "127.0.0.1",
    "database": "whatabook",
    "raise_on_warnings": True
}

""" function definitions """
def show_logo():
    print(
" _       ____          __        __                __" + "\n" +  
"| |     / / /_  ____ _/ /_____ _/ /_  ____  ____  / /__" + "\n" +
"| | /| / / __ \/ __ `/ __/ __ `/ __ \/ __ \/ __ \/ //_/" + "\n" +
"| |/ |/ / / / / /_/ / /_/ /_/ / /_/ / /_/ / /_/ / ,<   " + "\n" +
"|__/|__/_/ /_/\__,_/\__/\__,_/_.___/\____/\____/_/|_|  " + "\n" +
"-------------------EBENEZER EVANOFF--------------------" + "\n")


def user_input(num=None, user_ids=None, book_ids=None):
    """ A function to manage the user's input """

     # Set the number of attempts to 3
    attempts = 3

    while attempts > 0:
        # Loop until the user enters a valid choice or runs out of attempts
        try:
            for attempt in range(attempts):
                # If the user is in Main or Account Menu's, validate the user's choice is between 1 and the number of options
                if num is not None:
                    choice = int(input(f"[>] Enter your choice [1-{num}]: "))
                    if choice < 1 or choice > num:
                        attempts -= 1
                        if attempts > 0:
                            print(f"[!] Invalid choice. Please try again. Attempts remaining: {attempts}\n")
                        else:
                            print("[!] Too many failed attempts. Exiting program.\n")
                            sys.exit(0)
                    else:
                        return choice
                # If the user is in the Account Menu, validate the user's choice is in the list of valid user IDs
                elif user_ids is not None:
                    user_id = int(input('\n[>] Enter a customer id: '))
                    if user_id in user_ids:
                        return user_id
                    else:
                        attempts -= 1
                        if attempts > 0:
                            print(f"[!] Invalid customer id. Please try again. Attempts remaining: {attempts}\n")
                        else:
                            print("[!] Too many failed attempts. Exiting program.\n")
                            sys.exit(0)
                # If the user is in the Account Menu, validate the user's choice is in the list of valid book IDs
                elif book_ids is not None:
                    book_id = int(input('[>] Enter the ID of the book you would like to add to your wishlist: '))
                    if book_id in book_ids:
                        return book_id
                    else:
                        attempts -= 1
                        if attempts > 0:
                            print(f"[!] Invalid book id. Please try again. Attempts remaining: {attempts}\n")
                        else:
                            print("[!] Too many failed attempts. Exiting program.\n")
                            sys.exit(0)

        # If the user enters a non-integer value, display an error message and decrement the number of attempts
        except ValueError:
            attempts -= 1
            if attempts > 0:
                print(f"[!] Invalid choice. Please try again. Attempts remaining: {attempts}\n")
            else:
                print("[!] Too many failed attempts. Exiting program.\n")
                sys.exit(0)

def display_banner(text):
    """ A function to display a text banner """

    # Dictionary of symbols used to create the banner
    symbols = { "END": "-", "-": "+", "DISPLAYING BOOKS": "+", "DISPLAYING STORE LOCATIONS": "+", "DISPLAYING WISHLIST": "+", "MAIN MENU": "#", "ACCOUNT MENU": "#"}
    
    # Calculate the remaining length of the banner, where the dashes are displayed.
    total_length = 52 
    text_length = len(text) + 4  
    remaining_length = total_length - text_length

    # Check if the remaining length is even or odd, and set the number of dashes on the left and right sides accordingly
    if remaining_length % 2 == 0:
        dashes_left = dashes_right = remaining_length // 2
    else:
        dashes_left = remaining_length // 2
        dashes_right = dashes_left + 1

    # Construct banner and display it
    display = f'\n[{symbols[text]}]{ "-" * dashes_left } {text} { "-" * dashes_right }[{symbols[text]}]\n'

    print(display)
    
def display_continue():
    """ A function to display a continue message """

    input("[>] Press any key to continue: ")

def show_menu():
    """ A function to display the main menu """

    display_banner("MAIN MENU")
    print("[1] View Books\n[2] View Store Locations\n[3] My Account\n[4] Exit Program\n")

    return user_input(num=4) # Return the user's choice

def show_books(_cursor):
    """ A function to display all books in the database """

    # Select all books from the book table and include all columns.
    query = ("SELECT book_id, book_name, author, details from book") 
    _cursor.execute(query)

    # Get the results from the cursor object
    books = _cursor.fetchall()

    display_banner("DISPLAYING BOOKS")
    
    # Iterate over the query data set and display the results 
    for book in books:
        if book[3] is None:
            print(f"Title: {book[1]}\nAuthor: {book[2]}\n")
        else:
            print(f"Title: {book[1]}\nAuthor: {book[2]}\nDetails: {book[3]}\n")

    display_banner("END")
    display_continue()
  
def show_locations(_cursor):
    """ A function to display all store locations in the database """

    # Select all store locations from the store table and include all columns.
    query = ("SELECT store_id, locale from store")
    _cursor.execute(query)

    # Get the results from the cursor object
    locations = _cursor.fetchall()

    display_banner("DISPLAYING STORE LOCATIONS")

    # Iterate over the query data set and display the results 
    for location in locations:
        print(f"Locale: {location[1]}\n")

    display_banner("END")
    display_continue()

def validate_user(_cursor):
    """ A function to validate the user's ID """

    # Query the database for all user IDs
    _cursor.execute("SELECT user_id FROM user")

    # Get the results from the cursor object and store in a list
    users = [user[0] for user in _cursor.fetchall()]  # Used to validate the user's ID is in the database
    
    # Return the user's ID
    return user_input(user_ids=users)

def show_account_menu(_cursor, _user_id):
    """ A function to display the user's account menu """

    # Select the user's first and last name from the user table
    query = ("SELECT first_name, last_name from user WHERE user_id = %s")
    _cursor.execute(query, (_user_id,))

    # Get the results from the cursor object
    user = _cursor.fetchone()

    # Display the user's first and last name
    print(f"\n[+] Welcome back, {user[0].upper()} {user[1].upper()}!")

    # Display the user's account menu
    display_banner("ACCOUNT MENU")
    print("[1] Wishlist\n[2] Add Book\n[3] Main Menu\n")

    # Return the user's choice
    return user_input(num=3) 

def show_wishlist(_cursor, _user_id):
    """ A function to display the user's wishlist """

    # Select the user's wishlist from the wishlist table
    query = ("SELECT user.user_id, user.first_name, user.last_name, book.book_id, book.book_name, book.author " 
            "FROM wishlist "
            "INNER JOIN user ON wishlist.user_id = user.user_id " 
            "INNER JOIN book ON wishlist.book_id = book.book_id " 
            "WHERE user.user_id = %s")
    _cursor.execute(query, (_user_id,))

    # Get the results from the cursor object
    wishlist = _cursor.fetchall()

    display_banner("DISPLAYING WISHLIST")

    # Iterate over the query data set and display the results 
    for item in wishlist:
        print(f"Title: {item[4]}\nAuthor: {item[5]}\n")

    display_banner("END")
    display_continue()

def show_books_to_add(_cursor, _user_id):
    """ A function to display all books that the user can add to their wishlist """

    # Select all books from the book table that are not already in the user's wishlist
    query = ("SELECT book_id, book_name, author, details from book WHERE book_id NOT IN (SELECT book_id FROM wishlist WHERE user_id = %s)")
    _cursor.execute(query, (_user_id,))

    # Get the results from the cursor object
    books = _cursor.fetchall()

    display_banner("DISPLAYING BOOKS")

    # Store the book IDs and titles in separate lists
    book_ids = [book[0] for book in books] # Used to validate the user's choice
    titles = [book[1] for book in books] # Used to display the title of the book the user chose
    
    # Iterate over the query data set and display the results 
    for book in books:
        if book[3] is None:
            print(f"Book ID: {book[0]}\tTitle: {book[1]} --- Author: {book[2]}\n")
        else:
            print(f"Book ID: {book[0]}\tTitle: {book[1]} --- Author: {book[2]} --- Details: {book[3]}\n")

    display_banner("-")
    
    # Return the user's choice and the title of the book they chose
    choice = user_input(book_ids=book_ids)
    return choice, titles[book_ids.index(choice)]

def add_book_to_wishlist(_cursor, _user_id, _book_id, title):
    """ A function to add a book to the user's wishlist """

    # Insert the user's ID and the book's ID into the wishlist table
    query = ("INSERT INTO wishlist(user_id, book_id) VALUES (%s, %s)")
    _cursor.execute(query, (_user_id, _book_id))

    # Display a success message with the title of the book that was added to the user's wishlist
    print(f'\n[+] "{title}" was added to your wishlist!\n')
    display_banner("END")
    display_continue()

def main():
    """ The main function of the program """

    # Connect to the whatabook database
    try:
        # Unpack the config dictionary, create connection, and cursor objects
        db = mysql.connector.connect(**config)
        cursor = db.cursor()

        # Display the logo
        show_logo()

        # Display the main menu
        while True:
            choice = show_menu()

            # If the user chooses option 1, display all books in the database
            if choice == 1:
                show_books(cursor)

            # If the user chooses option 2, display all store locations in the database
            elif choice == 2:
                show_locations(cursor)

            # If the user chooses option 3, display the user's account menu
            elif choice == 3:
                user_id = validate_user(cursor)
                account_option = show_account_menu(cursor, user_id)

                # If the user chooses option 1, display the user's wishlist
                if account_option == 1:
                    show_wishlist(cursor, user_id)

                # If the user chooses option 2, display all books that the user can add to their wishlist
                elif account_option == 2:
                    book_id, title = show_books_to_add(cursor, user_id)
                    add_book_to_wishlist(cursor, user_id, book_id, title)
                    db.commit()

                # If the user chooses option 3, display the main menu
                elif account_option == 3:
                    continue

            # If the user chooses option 4, exit the program
            elif choice == 4:
                print("\n[+] Exiting program. Goodbye!\n")
                sys.exit(0)

    # If the connection to the database fails, display an error message and exit the program
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("\n[!] The supplied username or password are invalid. Please try again.\n")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("\n[!] The specified database does not exist. Please try again.\n")
        else:
            print(f"[!] {err}")
    finally:
        db.close()

if __name__ == "__main__":
    main()