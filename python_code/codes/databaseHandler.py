import mysql.connector
from codes.config import DATABASE_CONFIG


class databaseHandler:

    def __init__(self):
        self.con = mysql.connector.connect(
            host=DATABASE_CONFIG['host'],
            database=DATABASE_CONFIG['dbName'],
            user=DATABASE_CONFIG['user'],
            passwd=DATABASE_CONFIG['password']
        )
        self.cur = self.con.cursor()
        self.createSchemas()

    def createSchemas(self):
        self.cur.execute("CREATE DATABASE IF NOT EXISTS " + DATABASE_CONFIG['dbName'])
        for createRequest in DATABASE_CONFIG['createSchemas']:
            self.cur.execute(createRequest)

    def selectAllRecords(self):
        self.cur.execute("SELECT * FROM requests")
        return self.cur.fetchall()

    def selectAllOK(self):
        self.cur.execute("SELECT * FROM requests WHERE request_type = 'OK'")
        return self.cur.fetchall()

    def selectAllNotOK(self):
        self.cur.execute("SELECT * FROM requests WHERE request_type != 'OK'")
        return self.cur.fetchall()

    def selectAllOfType(self, requestType):
        self.cur.execute("SELECT * FROM requests WHERE request_type = '" + requestType + "'")
        return self.cur.fetchall()
