import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import KFold

def makeRequestSequenceOfChars(string):
    k = []
    for char in string:
        k.append(ord(char))
    length = len(k)
    t = [0 for i in range(256 - length)]  # fill the rest with 0, so as they will have same length
    return k + t

string = ["/api/v1/login/?customerId=1OR%201=1 HTTP/1.0",
          "/api/v1/register/%2e%2e%2f%2e%2e%2f%2e%2e%2ffile:///etc/passwd HTTP/1.1",
          "/update.php/.well-known/assetlinks.json HTTP/1.0", "/%2e%2e%2f%2e%2e%2f%2e%2e%2ffile:///etc/passwd HTTP/1.0"]




kf = KFold(n_splits=2)
X = np.array([makeRequestSequenceOfChars(i) for i in string])
y = np.array([[0,0],[1,1],[0,1],[1,0]])

for train_index, test_index in kf.split(X):
    print("TRAIN:", train_index, "TEST:", test_index)
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]
    classifier = Sequential()
    classifier.add(Dense(units=128, kernel_initializer="uniform", activation='relu', input_dim=256))
    classifier.add(Dense(units=128, kernel_initializer="uniform", activation='relu'))
    classifier.add(Dense(units=2, kernel_initializer="uniform", activation='softmax'))
    classifier.compile(optimizer="adam",loss="binary_crossentropy",metrics=['accuracy'])
    classifier.fit(X_train,y_train,batch_size=100,nb_epoch=100)
    y_pred = classifier.predict(X_test)
    y_pred=[[int(round(x[0])),int(round(x[1]))] for x in y_pred]
    counter = 0
    for index, element in enumerate(y_pred):
        if (element == y_test[index]).all():
            counter += 1
    print(counter / len(y_test))
    break