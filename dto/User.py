import mysql.connector

class User:
    def __init__(self, connectOption):
        self.db = mysql.connector.connect(
            host = connectOption['host'],
            user = connectOption['username'],
            password = connectOption['password'],
            database = connectOption['dbname']
        )
    def getUser(self, username):
        self.db.reconnect()
        sqlScript = "SELECT * FROM client_data WHERE user_id = '{0}'".format(username)
        cursor = self.db.cursor()
        cursor.execute(sqlScript)
        answer = cursor.fetchall()
        return answer


    def getUserByPhone(self, phone):
        self.db.reconnect()
        sqlScript = "SELECT * FROM client_data WHERE phone = '{0}'".format(phone)
        cursor = self.db.cursor()
        cursor.execute(sqlScript)
        answer = cursor.fetchall()
        return answer

    def updateUser(self, username, phone):
        self.db.reconnect()
        sqlScript = "UPDATE client_data SET user_id='{0}' WHERE phone = '{1}'".format(username, phone)
        print(sqlScript)
        cursor = self.db.cursor()
        answer = cursor.execute(sqlScript)
        self.db.commit()
        return



    def createUser(self, username, phone, task1, code):
        self.db.reconnect()
        sqlScript = "INSERT INTO client_data (role, task1, user_id, status, phone) VALUES ('4', '{0}', '{1}', '0', '{2}')".format(task1, username, phone)
        cursor = self.db.cursor()
        answer = cursor.execute(sqlScript)
        self.db.commit()

    def setCode(self, username, code):
        self.db.reconnect()
        sqlScript = "INSERT INTO code_access (phone, code) VALUES ('{0}', {1}) ".format(username, code)
        cursor = self.db.cursor()
        answer = cursor.execute(sqlScript)
        self.db.commit()


    def checkCode(self, username, code):
        self.db.reconnect()
        sqlScript = "SELECT * FROM code_access WHERE phone = '{0}' AND code = {1}".format(username, code)
        cursor = self.db.cursor()
        cursor.execute(sqlScript)
        answer = cursor.fetchall()
        return answer
