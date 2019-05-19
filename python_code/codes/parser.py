import apache_log_parser
import requests
import codes.databaseHandler as databaseHandler


def getTotalRequests():
    '''

    :param FileName:
    :return:
    '''
    db = databaseHandler.databaseHandler()
    return db.selectAllRecords()


def getTotalUniqueIps():
    db = databaseHandler.databaseHandler()
    return db.selectAllUniqueIps()


def getNotOkRequestsPerHour():
    db = databaseHandler.databaseHandler()
    result = db.selectAllNotOKPerHour()
    response=[dict() for i in range(24)]
    actualResponse = [[] for i in range(24)]
    for index, perHour in enumerate(result):
        for singleRequest in perHour:
            k = db.getCountryOfIp(singleRequest.remote_host)
            if k.country + ',' + k.code not in response[index]:
                response[index][k.country + ',' + k.code] = 0
            response[index][k.country + ',' + k.code] += 1

    for index, i in enumerate(response):
        for j in i:
            toAppend = j.split(',')
            toAppend.append(i[j])
            actualResponse[index].append(toAppend)

    return actualResponse

# getting the requests that got 5xx
def get5xxRequests(data):
    '''
    Get the 5xx requests
    :param data: total requests
    :return: the 5xx requets
    '''
    counter = 0
    for request in data:
        if 500 <= int(request.get("status")) < 600:
            counter += 1
    return counter


def getUniqueIPs(data):
    '''
    Get the unique ips from the total requests
    :param data: total requests
    :return: a array with all the unique ips
    '''
    unique_ips = set()
    for request in data:
        unique_ips.add(request.get("remote_host"))
    return unique_ips


def insertUniqueIps(unique_ips):
    for ip in unique_ips:
        URL = "http://ip-api.com/json/" + str(ip)
        r = requests.get(url=URL)
        data = r.json()
        db = databaseHandler.databaseHandler()
        db.insertUniqueIp(ip, data['country'], data['countryCode'])


def getRequestsPerIP(data, unique_ips=[]):
    '''

    :param data: total requests
    :param unique_ips: the list of the unique ips
    :return: the total requests for every ip
    '''
    if unique_ips == []:
        unique_ips = getUniqueIPs(data)
    unique_ips = list(unique_ips)
    requestPerIp = [0 for ip in unique_ips]
    for request in data:
        requestPerIp[unique_ips.index(request.get("remote_host"))] += 1
    return unique_ips,requestPerIp

def evaluate(normal, sqli,xss,lfi):
    return normal*1-(sqli+xss)*10-lfi*20

def getWorstCountry():
    db = databaseHandler.databaseHandler()
    data=db.getRequestTypesPerIp()
    results=[]
    for request in data:
        results.append([request.ip,int(evaluate(request.ok,request.sqli,request.xss,request.lfi))])
    worst=min([i[1] for i in results])
    ip=""
    for i in results:
        if i[1]==worst:
            ip=i[0]
            break
    for record in data:
        if record.ip==ip:
            return record
