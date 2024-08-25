import mysql.connector as mc 
conn = mc.connect(host ='localhost' , user = 'root' , password = 'root')

cur = conn.cursor()

create_database_query = "CREATE DATABASE IF NOT EXISTS userdb"
cur.execute(create_database_query)

conn.commit()

cur.close()
conn.close()

conn = mc.connect(host='localhost', user='root', password='root', database='userdb')

# Create a new cursor object
cur = conn.cursor()

# Create the table if it doesn't exist
create_table_query = """
CREATE TABLE IF NOT EXISTS customer_satisfaction (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    age INTEGER,
    flight_distance INTEGER,
    inflight_entertainment INTEGER,
    baggage_handling INTEGER,
    cleanliness INTEGER,
    departure_delay INTEGER,
    arrival_delay INTEGER,
    gender INTEGER,
    customer_type INTEGER,
    travel_type INTEGER,
    Class_Eco INTEGER DEFAULT 0,
    Class_Eco_Plus INTEGER DEFAULT 0
)
"""
cur.execute(create_table_query)

print("You have successfully created the 1st table in the database!") 

create_table_query = """
CREATE TABLE IF NOT EXISTS Prediction (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    output VARCHAR(15)
)
"""
cur.execute(create_table_query)
print("You have successfully created the 2nd table in the database!") 

# Close the cursor and connection
cur.close()
conn.close()