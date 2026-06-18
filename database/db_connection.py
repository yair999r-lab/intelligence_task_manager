import mysql.connector

class DB_connection:
    def __init__(self):
        self.connct = self.initial_connection()


    def initial_connection(self):
        return mysql.connector.connect(host="localhost", user="root",password='1234' ,port=3307)
    
    def create_database(self):
        cursor = self.connct.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS intelligence_db")
        cursor.execute("USE intelligence_db")
        cursor.close()


    def create_tabels(self):
        cursor = self.connct.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS agents(
                       id INT AUTO_INCREMENT PRIMARY KEY,
                       name VARCHAR(30) NOT NULL,
                       specialty VARCHAR(50) NOT NULL,
                       is_active BOOLEAN DEFAULT TRUE,
                       completed_mission INT DEFAULT 0,
                       failed_mission INT DEFAULT 0,
                       agent_renk ENUM ('Junior', 'Senior', 'Commander'))""")
        self.connct.commit()


        cursor.execute("""CREATE TABLE IF NOT EXISTS missions(
                        id INT AUTO_INCREMENT PRIMARY KEY,
                       title VARCHAR(30) NOT NULL,
                       description TEXT NOT NULL,
                       location VARCHAR(50) NOT NULL,
                       difficulty INT NOT NULL,
                       importance INT NOT NULL,
                       status VARCHAR(30) DEFAULT 'NEW',
                       risk_level VARCHAR(100) DEFAULT NULL,
                       assigned_agent_it INT DEFAULT NULL
)""")
        self.connct.commit()
        cursor.close()

    def get_connection(self):
        if not self.connct.is_connected():
            self.connct = self.initial_connection()
            self.create_database()
        return self.connct
        
db = DB_connection()