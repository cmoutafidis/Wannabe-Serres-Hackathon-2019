import mysql.connector
from codes.config import DATABASE_CONFIG
from codes.parserWithTime import getRequestsPerHour
import pycountry


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

    def selectAllNotOKPerHour(self):
        self.cur.execute("SELECT * FROM requests WHERE request_type != 'OK'")
        return getRequestsPerHour(self.getResults(self.cur))

    def selectAllOfType(self, requestType):
        self.cur.execute("SELECT * FROM requests WHERE request_type = '" + requestType + "'")
        return self.getResults(self.cur)

    def getResults(self, db_cursor):
        desc = [d[0] for d in db_cursor.description]
        results = [dotdict(dict(zip(desc, res))) for res in db_cursor.fetchall()]
        return results

    def updateRecordsType(self, records, type):
        ids = ", ".join(str(x) for x in records)
        self.cur.execute("UPDATE requests SET request_type = '" + type + "' WHERE id in (" + ids + ")")
        self.con.commit()

    def insertUniqueIp(self, ip, country, countryCode):
        cCode = pycountry.countries.get(alpha_2=countryCode).alpha_3
        self.cur.execute("INSERT INTO uniqueips (ip, country, totalRequests, code) VALUES (%s, %s, %s, %s)", (ip, country, 0, cCode))
        self.con.commit()

    def countUniqueIps(self):
        self.cur.execute("SELECT COUNT(*) as 'ipcount' from requests GROUP BY(remote_host)")
        return len(self.getResults(self.cur))

    def selectAllUniqueIps(self):
        self.cur.execute("SELECT country, sum(totalRequests) as 'totalReq' FROM uniqueips GROUP BY(country)")
        return self.getResults(self.cur)

    def getCountryOfIp(self, ip):
        self.cur.execute("SELECT country, code FROM uniqueips WHERE ip = '" + ip + "'")
        return self.getResults(self.cur)[0]

    def getCountryWithMostAttacks(self):
        self.cur.execute("SELECT country, count(ip) as totalCount FROM uniqueips INNER JOIN requests ON requests.remote_host = uniqueips.ip WHERE requests.request_type != 'OK' GROUP BY(country) ORDER BY totalCount DESC LIMIT 1")
        return self.getResults(self.cur)[0]


class dotdict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
