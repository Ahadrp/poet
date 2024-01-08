import mysql.connector

class Mysql:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.rows = None

    def handle_query(self, query: str):
        cnx = cursor = None
        try:
            cnx = mysql.connector.connect(host=self.host, user=self.user, password=self.password,
                                      database=self.database)
        except mysql.connector.Error as e:
            print(f"An error has occured while connecting to database: '{e}'")
            raise e

        try:
            cursor = cnx.cursor()
            cursor.execute(query)
        except mysql.connector.Error as e:
            print(f"An error has occured while sending query: '{e}'")
            raise e

        try:
            # Fetch all the rows returned by the query
            self.rows = cursor.fetchall()
        except mysql.connector.Error as e:
            print(f"An error has occured fetching data: '{e}'")
            raise e

        cnx.commit()
        cursor.close()
        cnx.close()

        return self.rows


