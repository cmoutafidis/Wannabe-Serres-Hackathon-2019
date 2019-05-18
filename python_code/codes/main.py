import codes.databaseHandler as databaseHandler
import codes.parser as parser


def executeFirstQuestion():
    printFirstQuestion((float(len(allNotOk)) / float(len(allRecords)))*100, parser.get5xxRequests(allRecords), db.countUniqueIps())


def printFirstQuestion(first, second, third):
    print('Γενικά: ')
    print(' 1: ' + str(format(first, ".2f")) + '%')
    print(' 2: ' + str(second))
    print(' 3: ' + str(len(third)))


db = databaseHandler.databaseHandler()
allNotOk = db.selectAllNotOK()
allRecords = db.selectAllRecords()
executeFirstQuestion()
