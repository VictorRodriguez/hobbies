import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn import svm
from random import randint

digits = datasets.load_digits()

#print(digits.data)         # Data of pictures of digits
#print(digits.target)       # Data of targets of those pictures
#print(digits.images[0])    # Image of the first element of digits 

rand_number = randint(-10,10)
print (rand_number)

clf = svm.SVC(gamma=0.001,C=100)
x,y = digits.data[:-10],digits.target[:-10]

clf.fit(x,y)

prediction = int(clf.predict(digits.data[rand_number]))

print("Predicted Number = %d" % (prediction))

if prediction == digits.target[rand_number]: 
    print("TRUE")
    ret = 0
else:
    print("FALSE")
    ret = 1

plt.imshow(digits.images[rand_number],cmap=plt.cm.gray_r,interpolation="nearest")
plt.show()
