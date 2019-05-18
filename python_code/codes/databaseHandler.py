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
        return self.getResults(self.cur)

    def selectAllOK(self):
        self.cur.execute("SELECT * FROM requests WHERE request_type = 'OK'")
        return self.getResults(self.cur)

    def selectAllNotOK(self):
        self.cur.execute("SELECT * FROM requests WHERE request_type != 'OK'")
        return self.getResults(self.cur)

    def selectAllOfType(self, requestType):
        self.cur.execute("SELECT * FROM requests WHERE request_type = '" + requestType + "'")
        return self.getResults(self.cur)

    def getResults(self, db_cursor):
        desc = [d[0] for d in db_cursor.description]
        results = [dotdict(dict(zip(desc, res))) for res in db_cursor.fetchall()]
        return results


class dotdict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
