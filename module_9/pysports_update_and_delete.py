""" 
    Title: pysports_update_and_delete.py
    Author: Ebenezer Evanoff
    Date: 01 December 2023
    Description: Test program for inserting, updating, and deleting records from the pysports database
"""

""" import statements """
import argparse
import mysql.connector
from mysql.connector import errorcode

""" argument parser configuration """
parser = argparse.ArgumentParser()
parser.add_argument("--first_name", help="The player's first name")
parser.add_argument("--last_name", help="The player's last name")
parser.add_argument("--team_id", help="The player's team ID number")
args = parser.parse_args()

""" global variables """
first_name = args.first_name
last_name = args.last_name
team_id = args.team_id

""" database config object """
config = {
    "user": "pysports_user",
    "password": "MySQL8IsGreat!",
    "host": "127.0.0.1",
    "database": "pysports",
    "raise_on_warnings": True
}


def show_players(cursor, title):
    """ method to execute an inner join on the player and team table, 
        iterate over the dataset and output the results to the terminal window.
    """

    # inner join query 
    cursor.execute("SELECT player_id, first_name, last_name, team_name FROM player INNER JOIN team ON player.team_id = team.team_id")

    # get the results from the cursor object 
    players = cursor.fetchall()

    print("\n  -- {} --".format(title))
    
    # iterate over the player data set and display the results 
    for player in players:
        print("  Player ID: {}\n  First Name: {}\n  Last Name: {}\n  Team Name: {}\n".format(player[0], player[1], player[2], player[3]))

try:
    """ try/catch block for handling potential MySQL database errors """ 

    db = mysql.connector.connect(**config) # connect to the pysports database 

    # get the cursor object
    cursor = db.cursor()

    # insert player query 
    add_player = ("INSERT INTO player(first_name, last_name, team_id)"
                 "VALUES(%s, %s, %s)")

    # player data fields 
    player_data = (first_name, last_name, team_id)

    # insert a new player record
    cursor.execute(add_player, player_data)

    # commit the insert to the database 
    db.commit()

    # show all records in the player table 
    show_players(cursor, "DISPLAYING PLAYERS AFTER INSERT")

    # get the player ID from the last insert statement
    player_id = cursor.lastrowid

    # update the newly inserted record 
    update_player = (f"UPDATE player SET team_id = 2, first_name = 'Gollum', last_name = 'Ring Stealer' WHERE first_name = '{first_name}'")

    # execute the update query
    cursor.execute(update_player)

    # show all records in the player table 
    show_players(cursor, "DISPLAYING PLAYERS AFTER UPDATE")

    # delete query using player_id from the last insert statement
    delete_player = ("DELETE FROM player WHERE player_id = %s")

    # note the trailing comma after player_id --> this is required for the single value tuple
    cursor.execute(delete_player, (player_id,)) 

    # show all records in the player table 
    show_players(cursor, "DISPLAYING PLAYERS AFTER DELETE")

    input("\n\n  Press any key to continue... ")

except mysql.connector.Error as err:
    """ handle errors """ 
    

    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist")

    else:
        print(err)

finally:
    """ close the connection to MySQL """

    db.close()