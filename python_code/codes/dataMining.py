import operator
from urllib.parse import unquote

restrictedSQLInjectionCharacters = ["'", ' or ', ' and ']
restrictedXSSCharacters = ['http://', 'https://', '<script', 'script>', '<?php', '?>']
restrictedLFICharacters = ['../', '\\x', 'ls+-l']


def getSQLInjectionRequests(data):
    curDict = getMatchesInListWithoutStringStrip(data, restrictedSQLInjectionCharacters)
    return curDict


def getXSSRequests(data):
    curDict = getMatchesInList(data, restrictedXSSCharacters)
    return curDict


def getLFIRequests(data):
    curDict = getMatchesInList(data, restrictedLFICharacters)
    return curDict


def getMatchesInList(data, restrictDict):
    curDict = dict()
    for index, request in enumerate(data):
        for restrictedChar in restrictDict:
            if restrictedChar in unquote(request.get('request_url_query')).replace(" ", "").lower():
                curDict[str(index)] = request.get('id')
                break
    return curDict


def getMatchesInListWithoutStringStrip(data, restrictDict):
    curDict = dict()
    for index, request in enumerate(data):
        for restrictedChar in restrictDict:
            if restrictedChar in unquote(request.get('request_url_query')).lower():
                curDict[str(index)] = request.get('id')
                break
    return curDict


def printMatches(curDict):
    for request in curDict:
        print(curDict.get(request))


def getUniqueAttackRequests(sqlDict, xssDict, lfiDict):
    uniqueRequests = set()
    for item in sqlDict.keys():
        uniqueRequests.add(item)
    for item in xssDict.keys():
        uniqueRequests.add(item)
    for item in lfiDict.keys():
        uniqueRequests.add(item)
    return uniqueRequests


def getPercentageOfServerAttackRequests(uniqueRequests,data):
    return float(len(uniqueRequests))/float(len(data)) * 100


def getMostAttackedWebsites(uniqueRequests,data):
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


