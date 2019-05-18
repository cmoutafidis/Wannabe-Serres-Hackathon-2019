import operator
from codes.parser import getTotalRequests
from urllib.parse import unquote

restrictedSQLInjectionCharacters = ["'", ' or ', ' and ']
restrictedXSSCharacters = ['http://', 'https://', '<script', 'script>', '<?php', '?>']
restrictedLFICharacters = ['../', '\\x', 'ls+-l']


def getSQLInjectionRequests():
    curDict = getMatchesInListWithoutStringStrip(restrictedSQLInjectionCharacters)
    # printMatches(curDict)
    return curDict


def getXSSRequests():
    curDict = getMatchesInList(restrictedXSSCharacters)
    # printMatches(curDict)
    return curDict


def getLFIRequests():
    curDict = getMatchesInList(restrictedLFICharacters)
    # printMatches(curDict)
    return curDict


def getMatchesInList(restrictDict):
    curDict = dict()
    for index, request in enumerate(data):
        for restrictedChar in restrictDict:
            if restrictedChar in unquote(request.get('request_url_query')).replace(" ", "").lower():
                curDict[str(index)] = unquote(request.get('request_url'))
                break
    return curDict


def getMatchesInListWithoutStringStrip(restrictDict):
    curDict = dict()
    for index, request in enumerate(data):
        for restrictedChar in restrictDict:
            if restrictedChar in unquote(request.get('request_url_query')).lower():
                curDict[str(index)] = unquote(request.get('request_url'))
                break
    return curDict


def printMatches(curDict):
    for request in curDict:
        print(curDict.get(request))


def loadData():
    return getTotalRequests('../daily-logs/website-access.log.')


def getUniqueAttackRequests(sqlDict, xssDict, lfiDict):
    uniqueRequests = set()
    for item in sqlDict.keys():
        uniqueRequests.add(item)
    for item in xssDict.keys():
        uniqueRequests.add(item)
    for item in lfiDict.keys():
        uniqueRequests.add(item)
    return uniqueRequests


def getPercentageOfServerAttackRequests(uniqueRequests):
    return float(len(uniqueRequests))/float(len(data)) * 100


def getMostAttackedWebsites(uniqueRequests):
    maxims = dict()
    websites = dict()
    for item in uniqueRequests:
        curList = data[int(item)].get('request_url_path').split('/')
        curList = curList[:-1]
        path = '/'.join(str(x) for x in curList)
        path += '/'
        if path not in websites:
            websites[path] = 0
        websites[path] += 1

    for i in range(0, 5):
        nextKey = (max(websites.items(), key=operator.itemgetter(1))[0])
        maxims[nextKey] = websites[nextKey]
        websites[nextKey] = 0

    return maxims


data = loadData()
print('Data are loaded')
sqlDict = getSQLInjectionRequests()
xssDict = getXSSRequests()
lfiDict = getLFIRequests()

print('Data len: ' + str(len(data)))
print('SQL Injection Requests: ' + str(len(sqlDict.keys())))
print('XSS Requests: ' + str(len(xssDict.keys())))
print('LFI Requests: ' + str(len(lfiDict.keys())))

uniqueRequests = getUniqueAttackRequests(sqlDict, xssDict, lfiDict)

print('Percentage of requests that are attacks: ' + format(getPercentageOfServerAttackRequests(uniqueRequests), '.2f') + "%")
maxims = getMostAttackedWebsites(uniqueRequests)

print('Most Visited Websites:')
for item in maxims:
    print(item + ": " + str(maxims.get(item)))
