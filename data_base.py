import mysql.connector

# MySQL configuration

user_name = "web204_1"
password = "<5FDkDH9P=GwFPyH"
host = "s272.goserver.host"
port = 3306
db_name = "web204_db1"
tablename = "members_links"


# Connect to the database

def connection(user_id):
    try:
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
        user_links_list = function_1(results, user_id)

        print(user_links_list)

        cursor.close()
        cnx.close()

        return user_links_list
        # Close the cursor and connection

    except Exception as ex:
        print("An error while connecting to db.")


def function_1(results, user_id):

    user_links_list = []
    for row in results:
        logged_user_id = row[6]  # Extract the user_id index 0
        link = row[3]  # Extract the link

        if user_id == logged_user_id:
            user_links_list.append(link)
        else:
            # user_links_list.append(link)
            pass
    # user_links_list.append("https://www.kleinanzeigen.de/s-berlin/bmw/k0l3331")
    return user_links_list


# if __name__ == '__main__':
#     connection("1421290036")
