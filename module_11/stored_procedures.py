""" import statements """
import argparse
import mysql.connector
from mysql.connector import errorcode

""" argument parser configuration """
parser = argparse.ArgumentParser()
parser.add_argument("--get_rentals", type=str, help="Filter film rentals" )
parser.add_argument("--stored_procedure", type=str, help="Execute stored procedure")
args = parser.parse_args()

""" global variables """
filter = args.get_rentals
sp_filter = args.stored_procedure

""" database config object """
config = {
    "user": "sakila_user",
    "password": "sakila",
    "host": "127.0.0.1",
    "database": "sakila",
    "raise_on_warnings": True
}

try:
    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    if args.get_rentals:
        filter = args.get_rentals
        query = ("SELECT film.title, COUNT(rental.inventory_id) AS total_rentals "
                 "FROM film "
                 "JOIN inventory ON film.film_id = inventory.film_id "
                 "JOIN rental ON inventory.inventory_id = rental.inventory_id "
                 "GROUP BY film.title "
                 "HAVING film.title LIKE %s "
                 "ORDER BY total_rentals DESC;")
        cursor.execute(query, (f"{filter}%",))
        for result in cursor.fetchall():
            print(result[1], "\t", result[0])

    elif args.stored_procedure:
        sp_filter = args.stored_procedure
        cursor.callproc("GetFilmRentals", [sp_filter])
        for result in cursor.stored_results():
            for row in result.fetchall():
                print(row[1], "\t", row[0])

    else:
        print("Please enter a valid command.")
        quit()

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("The supplied username or password are invalid")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("The specified database does not exist")

    else:
        print(err)

finally:
    if 'db' in locals() or 'db' in globals():
        db.close()




