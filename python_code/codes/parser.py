import apache_log_parser
import requests
import codes.databaseHandler as databaseHandler


# from pprint import pprint

def getTotalRequests():
    '''

    :param FileName:
    :return:
    '''
    db = databaseHandler.databaseHandler()
    return db.selectAllOK()


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


# data = getTotalRequests()
# insertUniqueIps(getUniqueIPs(data))
#
# print("Total number of requests: "+str(len(data)))
# print("Number of 5xx requests: " + str(get5xxRequests(data)))
# for ip in getUniqueIPs(data):
#     print(ip)
