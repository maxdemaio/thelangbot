import os
import mysql.connector
import time
import tweepy

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Setup MySQL db
mydb = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    database=os.getenv("DB_DB"))
mycursor = mydb.cursor()



mycursor.execute("SELECT * FROM patreon WHERE twitterUser = %s", ("maxwelldemaio",))
myresult = mycursor.fetchall()
print(len(myresult))


mycursor.close()
mydb.close()
