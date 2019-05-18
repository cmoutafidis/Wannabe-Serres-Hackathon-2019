import numpy as np
from sklearn.cluster import KMeans
import codes.databaseHandler as databaseHandler
import matplotlib.pyplot as plt

def makeRequestSequenceOfChars(string):
    k=[]
    for char in string:
        k.append(ord(char))
    length=len(k)
    t=[0 for i in range(256-length)] # fill the rest with 0, so as they will have same length
    return k+t

def stringsTO10Array(string):
    chars=["'", ' or ', ' and ','http://', 'https://', '<script', 'script>', '<?php', '?>','../', '\\x', 'ls+-l']
    answer=[]
    for char in chars:
        if char in string:
            answer.append(1)
        else:
            answer.append(0)
    return answer

dh=databaseHandler.databaseHandler()
X=[]
y=[]
data=dh.selectAllRecords()
for element in data:
    X.append(stringsTO10Array(element.request_url))
    y.append(element.request_type)

X=np.array(X)
wcss=[]
for i  in range(1,11):
    print(i)
    kmeans=KMeans(n_clusters=i,init="k-means++",max_iter=300,n_init=10)
    kmeans.fit(X=X)
    wcss.append(kmeans.inertia_)
plt.plot(range(1,11),wcss)
plt.title('The Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.savefig('elbow_Method.png', dpi=400)
plt.show()


kmeans=KMeans(n_clusters=4,init="k-means++",max_iter=300,n_init=10)
y_kmeans=kmeans.fit_predict(X)
