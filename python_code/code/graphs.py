from code.parserWithTime import getRequestsPerHour
from code.parser import getTotalRequests
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


data = getTotalRequests("../daily-logs/website-access.log.")
perHour = getRequestsPerHour(data)
getBarGraphRequestsPerHour(perHour)
