import codes.databaseHandler as databaseHandler
import codes.parser as parser
import codes.parserWithTime as ptime
import codes.dataMining as dm
import codes.graphs as graphs
import datetime


def executeFirstQuestion(allRecords):
    printFirstQuestion(len(allRecords), parser.get5xxRequests(allRecords), db.countUniqueIps())


def printFirstQuestion(first, second, third):
    print('Γενικά: ')
    print(' Συνολικό traffic: ' + str(format(first)))
    print(' Σύνολο 5xx Requests: ' + str(second))
    print(' Σύνολο μοναδικών IPs: ' + str(third))


def executeSecondQuestion(allRecords,allNotOK,db):
    sqlDict = dm.getSQLInjectionRequests()
    xssDict = dm.getXSSRequests()
    lfiDict = dm.getLFIRequests()

    uniqueRequests = dm.getUniqueAttackRequests(sqlDict, xssDict, lfiDict)
    print('Data Mining: ')

    print('Percentage of requests that are attacks: ' + format(dm.getPercentageOfServerAttackRequests(uniqueRequests,allRecords),
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
    print("Bar Graph for Requests per Hour has been created")
    # create the bar graph with requests/hour and save it @ RequestsPerHour_Bar.png
    graphs.getPieGraphForAllTheRequestsPerIp()
    print


db = databaseHandler.databaseHandler()
allNotOk = db.selectAllNotOK()
allRecords = db.selectAllRecords()





executeFirstQuestion(allRecords)
executeSecondQuestion(allRecords,allNotOk,db)
