import mysql.connector

class Utils:
    # Get the blacklist as a set of strings.
    def getBlacklist(mycursor) -> set:
        if mycursor == None:
            return set([])
        mycursor.execute(
            "SELECT * FROM blacklist")
        myresult = mycursor.fetchall()
        # Convert list of tuples to set of strings
        # row[1] has the username row[0] is the primary key
        usernames = set([row[1] for row in myresult])
        return usernames 
            
    # Get the supporters as a set of strings.
    def getSupporters(mycursor) -> set:
        if mycursor == None:
            return set([])
        mycursor.execute(
            "SELECT * FROM supporter")
        myresult = mycursor.fetchall()
        # Convert list of tuples to set of strings
        # row[1] has the username row[0] is the primary key
        usernames = set([row[1] for row in myresult])
        return usernames

    # Get last seen Tweet id
    def retrieveLastSeenId(mycursor) -> int:
        if mycursor == None:
            return 0
        mycursor.execute("SELECT * FROM tweet")
        myresult = mycursor.fetchall()
        return myresult[0][1]

    # Store the last retweeted Tweet in the DB
    def storeLastSeenId(mydb, mycursor, lastSeenId: int) -> None:
        if mycursor == None:
            return
        exampleId: int = (lastSeenId)
        mycursor.execute("UPDATE tweet SET tweetId = '%s' WHERE id = 1", (exampleId,))
        mydb.commit()
        print(mycursor.rowcount, "record(s) affected", flush=True)
        return