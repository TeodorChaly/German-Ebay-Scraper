import mysql.connector

# MySQL configuration
user_name = "name"
password = "password"
host = "host"
port = 3306
db_name = "db name"
tablename = "members_links"

# Connect to the database
cnx = mysql.connector.connect(
    user=user_name,
    password=password,
    host=host,
    port=port,
    database=db_name
)

# Create a cursor object to execute SQL queries
cursor = cnx.cursor()

# Execute a sample query
query = "SELECT * FROM {table};".format(table=tablename)
cursor.execute(query)

# Fetch all the results
results = cursor.fetchall()

# Process the results
full_dict = {}
for row in results:

    logged_user_id = row[6]  # Extract the user_id index 0
    link = row[3]  # Extract the link



    print("Full:", logged_user_id)
    print("Link:", link)

# Close the cursor and connection
cursor.close()
cnx.close()
