import pymysql

class DatabaseConnector:
    def __init__(self, config):
        self.host = config['host']
        self.port = int(config['port'])
        self.user = config['user']
        self.password = config['password']
        self.database = config['database']
        self.connection = None

    def connect(self):
        try:
            self.connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Connected to the database!")
        except pymysql.Error as e:
            print(f"Error connecting to the database: {e}")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Disconnected from the database.")

    def execute_query(self, query, values=None):
        try:
            with self.connection.cursor() as cursor:
                if values is None:
                    cursor.execute(query)
                else:
                    cursor.execute(query, values)
                result = cursor.fetchall()
                return result
        except pymysql.Error as e:
            print(f"Error executing query: {e}")

    
    
    def execute_insert(self, query, values):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, values)
                self.connection.commit()
                print("Insert successful.")
        except pymysql.Error as e:
            print(f"Error executing insert query: {e}")
            self.connection.rollback()