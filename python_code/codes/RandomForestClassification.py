import numpy as np
from sklearn.model_selection import KFold
from sklearn.metrics import confusion_matrix

kf = KFold(n_splits=2)

string = ["/api/v1/login/?customerId=1OR%201=1 HTTP/1.0",
          "/api/v1/register/%2e%2e%2f%2e%2e%2f%2e%2e%2ffile:///etc/passwd HTTP/1.1",
          "/update.php/.well-known/assetlinks.json HTTP/1.0", "/%2e%2e%2f%2e%2e%2f%2e%2e%2ffile:///etc/passwd HTTP/1.0"]


def makeRequestNumberic(string):
    k = [0 for i in range(255)]
    for char in string:
        k[ord(char)] += 1
    return k

def makeRequestSequenceOfChars(string):
    k=[]
    for char in string:
        k.append(ord(char))
    length=len(k)
    t=[0 for i in range(256-length)] #fill the rest with 0, so as they will have same length
    return k+t


# X = np.array([makeRequestNumberic(i) for i in string])
X = np.array([makeRequestSequenceOfChars(i) for i in string])
y = np.array([[0,0],[1,1],[0,1],[1,0]])
# create classifier
from sklearn.ensemble import RandomForestClassifier

for train_index, test_index in kf.split(X):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]
    classifier = RandomForestClassifier(n_estimators=10, criterion='entropy')
    classifier.fit(X_train, y_train)
    y_pred = classifier.predict(X_test)
    counter=0
    for index,element in enumerate(y_pred):
        if (element==y_test[index]).all():
            counter+=1
    print(counter/len(y_test))