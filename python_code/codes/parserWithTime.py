from codes.parser import getTotalRequests
import datetime


def getRequestsPerHour(data):
    '''
    Return an array with the amount of requests per server-hour
    :param data: total requests
    :return: requests pre hour
    '''
    requestsPerHour = [0 for i in range(24)]
    for request in data:
        requestsPerHour[
            datetime.datetime.strptime(request.get('time_received_tz_isoformat'), "%Y-%m-%dT%H:%M:%S+02:00").hour] += 1
    return requestsPerHour


# data = getTotalRequests("../daily-logs/website-access.log.")

# for hour in getRequestsPerHour(data):
#     print(hour)

# print(sum(getRequestsPerHour(data)))
# print(data[0].keys())
# print(data[0].values())
# print(len(data))
