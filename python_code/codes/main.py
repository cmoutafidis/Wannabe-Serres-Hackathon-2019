import codes.databaseHandler as databaseHandler
import codes.parser as parser
import codes.parserWithTime as ptime
import codes.dataMining as dm
import codes.graphs as graphs


def executeFirstQuestion(allRecords):
    printFirstQuestion(len(allRecords), parser.get5xxRequests(allRecords), db.countUniqueIps())


def printFirstQuestion(first, second, third):
    print('Γενικά: ')
    print(' Συνολικό traffic: ' + str(format(first)))
    print(' Σύνολο 5xx Requests: ' + str(second))
    print(' Σύνολο μοναδικών IPs: ' + str(third))


def executeSecondQuestion(allRecords, allNotOK, db):
    sqlDict = dm.getSQLInjectionRequests(allRecords)
    xssDict = dm.getXSSRequests(allRecords)
    lfiDict = dm.getLFIRequests(allRecords)

    uniqueRequests = dm.getUniqueAttackRequests(sqlDict, xssDict, lfiDict)
    print('Data Mining: ')

    print('Percentage of requests that are attacks: ' + format(dm.getPercentageOfServerAttackRequests(uniqueRequests, allRecords),
                                                               '.2f') + "%")
    print('SQL Injection Requests: ' + str(len(sqlDict.keys())))
    print('XSS Requests: ' + str(len(xssDict.keys())))
    print('LFI Requests: ' + str(len(lfiDict.keys())))

    # db.updateRecordsType(sqlDict.values(), 'SQLI')
    # db.updateRecordsType(xssDict.values(), 'XSS')
    # db.updateRecordsType(lfiDict.values(), 'LFI')


    maxims = dm.getMostAttackedWebsites(uniqueRequests,allRecords)

    print('Most Attacked Websites:')
    for item in maxims:
        print("  "+item + ": " + str(maxims.get(item)))

    mostAttacks=db.getCountryWithMostAttacks()
    print('Country with most attacks is '+mostAttacks.country+" with "+str(mostAttacks.totalCount)+" attacks")


def executeThirdQuestion(allRecords):
    print("Visualization :")
    #create the bar graph with requests/hour and save it @ RequestsPerHour_Bar.png
    graphs.getBarGraphRequestsPerHour(ptime.getAllRequestsPerHour(allRecords))
    print(" Bar Graph for Requests per Hour has been created")
    # create the pie graph with requests/country and save it @ RequestsPerCountry_PieChart
    graphs.getPieGraphForAllTheRequestsPerIp()
    print(" Pie Chart for requests per Country has been created ")
    # create the 24 html files, world map with countries request / hour
    graphs.worldGraph()
    print(" HTML files for World Graphs has been created")

def executeWorstIp():
    record=parser.getWorstCountry()
    print("Most harmful ip is "+record.ip+" with:\n "+str(record.ok)+" Normal Requests,\n "+str(record.sqli)+" SQL Injection requests,\n "+str(record.xss)+" XSS requests,\n "+str(record.lfi)+" Local File Injection requests,\n")


db = databaseHandler.databaseHandler()
allNotOk = db.selectAllNotOK()
allRecords = db.selectAllRecords()

executeFirstQuestion(allRecords)
executeSecondQuestion(allRecords, allNotOk, db)
executeThirdQuestion(allRecords)
executeWorstIp()