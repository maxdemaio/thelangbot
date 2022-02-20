import mysql.Cursor as Cursor
import mysql.connection.MySQLConnection as Connection

# Get the blacklist as a set of strings.
def getBlacklist(mycursor: Cursor) -> set:
    mycursor.execute(
        "SELECT * FROM blacklist")
    myresult = mycursor.fetchall()
    # Convert list of tuples to set of strings
    usernames = set([row[0] for row in myresult])
    return usernames 
        
# Get the supporters as a set of strings.
def getSupporters(mycursor: Cursor) -> set:
    mycursor.execute(
        "SELECT * FROM supporter")
    myresult = mycursor.fetchall()
    # Convert list of tuples to set of strings
    usernames = set([row[0] for row in myresult])
    return usernames

# Get last seen Tweet id
def retrieveLastSeenId(mycursor: Cursor) -> int:
    mycursor.execute("SELECT * FROM tweet")
    myresult = mycursor.fetchall()
    return myresult[0][1]

# Store the last retweeted Tweet in the DB
def storeLastSeenId(mydb: Connection, mycursor: Cursor, lastSeenId: int) -> None:
    exampleId: int = (lastSeenId)
    mycursor.execute("UPDATE tweet SET tweetId = '%s' WHERE id = 1", (exampleId,))
    mydb.commit()
    print(mycursor.rowcount, "record(s) affected", flush=True)
    return