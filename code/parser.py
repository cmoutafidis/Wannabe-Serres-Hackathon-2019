import apache_log_parser
# from pprint import pprint

def getTotalRequests(FileName):
    '''

    :param FileName:
    :return:
    '''
    file = open(FileName, 'r')
    line_parser = apache_log_parser.make_parser("%h %l %u %t \"%r\" %>s %b")
    data = []
    for line in file:
        log_line_data = line_parser(line)
        data.append(log_line_data)
    return data


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


data = getTotalRequests("access_log")

# print("Total number of requests: "+str(len(data)))
# print("Number of 5xx requests: " + str(get5xxRequests(data)))
# for ip in getUniqueIPs(data):
#     print(ip)
