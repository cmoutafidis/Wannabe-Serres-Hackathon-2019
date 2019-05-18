from code.parserWithTime import getRequestsPerHour
from code.parser import getRequestsPerIP
from code.parser import getTotalRequests
from code.parser import mapIpsToCountries
import matplotlib.pyplot as plt

plt.rcdefaults()
import numpy as np


def getBarGraphRequestsPerHour(perHour):
    objects = [i for i in range(24)]
    y_pos = np.arange(len(perHour))
    plt.bar(y_pos, perHour, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylim(bottom=min(perHour) - 5, top=max(perHour) + 3)
    plt.ylabel('Requests')
    plt.title('Requests per Hour')
    plt.savefig('RequestsPerHour_BarGraph.png', dpi=400)


def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
    return my_autopct

def getPieGraphForAllTheRequestsPerIp(unique_ips, requestsPerIp, dictOfCountries):
    countries = [country for country in dictOfCountries.keys()]
    requestsPerCountry = [0 for i in countries]
    for index,country in enumerate(countries):
        ips = dictOfCountries[country]
        for ip in ips:
            requestsPerCountry[index]+=requestsPerIp[unique_ips.index(ip)]
    fig1, ax1 = plt.subplots()
    explode=[0.1 if k == max(requestsPerCountry) else 0 for k in requestsPerCountry]
    ax1.pie(requestsPerCountry,  labels=countries, autopct=make_autopct(requestsPerCountry), explode=explode,
            shadow=False, startangle=90)
    # ax1.pie(requestsPerCountry, labels=countries, autopct="%1.1f%%", explode=explode,
    #        shadow=False, startangle=90)
    ax1.axis('equal')
    plt.title("Percentage requests per  country",bbox={'facecolor':'0.8', 'pad':5})
    plt.savefig('RequestsPerCountry_PieChart.png', dpi=400)




# data = getTotalRequests("../daily-logs/website-access.log.")
# perHour = getRequestsPerHour(data)
# getBarGraphRequestsPerHour(perHour)
# unique,requestsIP=getRequestsPerIP(data)
# getPieGraphForAllTheRequestsPerIp(unique,requestsIP,mapIpsToCountries(unique))
