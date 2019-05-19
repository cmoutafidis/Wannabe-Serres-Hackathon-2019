from codes.parser import getTotalRequests, getTotalUniqueIps, getNotOkRequestsPerHour
from codes.parserWithTime import getAllRequestsPerHour
import matplotlib.pyplot as plt

plt.rcdefaults()
import numpy as np
import plotly
import plotly.graph_objs as go
import pandas as pd
import pycountry


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
        val = int(round(pct * total / 100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct, v=val)

    return my_autopct


def reqsPerCountry(data):
    countries = []
    requestsPerCountry = []
    for d in data:
        countries.append(d.country)
        requestsPerCountry.append(int(d.totalReq))

    return countries, requestsPerCountry


def getPieGraphForAllTheRequestsPerIp():
    data = getTotalUniqueIps()
    countries, requestPerCountry = reqsPerCountry(data)
    fig1, ax1 = plt.subplots()
    explode = [0.1 if k == max(requestPerCountry) else 0 for k in requestPerCountry]
    ax1.pie(requestPerCountry, labels=countries, autopct=make_autopct(requestPerCountry), explode=explode,
            shadow=False, startangle=90)
    # ax1.pie(requestsPerCountry, labels=countries, autopct="%1.1f%%", explode=explode,
    #        shadow=False, startangle=90)
    ax1.axis('equal')
    plt.title("Percentage requests per  country", bbox={'facecolor': '0.8', 'pad': 5})
    plt.savefig('RequestsPerCountry_PieChart.png', dpi=400)


def getDataFrame(beforeDataFrame):
    # Append the rest with 0
    df = pd.DataFrame(beforeDataFrame, columns=['Country', 'Code', 'Requests'])
    for i in range(len(pycountry.countries)):
        country=list(pycountry.countries)[i]
        if df.loc[df['Code'] == country.alpha_3].empty:
            temp=pd.DataFrame([[country.name,country.alpha_3,0]], columns=['Country', 'Code', 'Requests'])
            df=pd.concat([df,temp])
    return df


def worldGraph():
    data = getNotOkRequestsPerHour()
    for index,hour in enumerate(data):
        df = getDataFrame(hour)
        data = [go.Choropleth(
            locations=df['Code'],
            z=df['Requests'],
            text=df['Country'],
            colorscale=[
                [0, "rgb(5, 10, 172)"],
                [0.35, "rgb(40, 60, 190)"],
                [0.5, "rgb(70, 100, 245)"],
                [0.6, "rgb(90, 120, 245)"],
                [0.7, "rgb(106, 137, 247)"],
                [1, "rgb(220, 220, 220)"]
            ],
            autocolorscale=False,
            reversescale=True,
            marker=go.choropleth.Marker(
                line=go.choropleth.marker.Line(
                    color='rgb(180,180,180)',
                    width=0.5
                )),
            colorbar=go.choropleth.ColorBar(
                tickprefix='',
                title='Amount of Requests'),
        )]

        layout = go.Layout(
            title=go.layout.Title(
                text='Requests to Server @'+str(index+1)+" hour of the day"
            ),
            geo=go.layout.Geo(
                showframe=False,
                showcoastlines=False,
                projection=go.layout.geo.Projection(
                    type='equirectangular'
                )
            ),
            annotations=[go.layout.Annotation(
                x=0.55,
                y=0.1,
                xref='paper',
                yref='paper',
                text='Source: ',
                showarrow=False
            )]
        )

        fig = go.Figure(data=data, layout=layout)
        plotly.offline.plot(fig, filename='d3-world-map'+str(index))


data = getTotalRequests()
# getBarGraphRequestsPerHour(getAllRequestsPerHour(data))
getPieGraphForAllTheRequestsPerIp()
# worldGraph()
