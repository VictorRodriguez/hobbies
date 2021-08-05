import pandas as pd
import wikipedia
articles=['Data Science','Artificial intelligence',
          'European Central Bank',
          'Basketball','Swimming']
wiki_lst=[]
title=[]
for article in articles:
    print("loading content: ",article)
    try:
        wiki_lst.append(wikipedia.page(article).content)
    except wikipedia.exceptions:
        continue
    title.append(article)
print("examine content")
wiki_lst

from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(stop_words={'english'})
X = vectorizer.fit_transform(wiki_lst)
#print(vectorizer.get_feature_names())
print(X.shape)

import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

Sum_of_squared_distances = []
K = range(2,5)
for k in K:
    km = KMeans(n_clusters=k, max_iter=200, n_init=10)
    km = km.fit(X)
    Sum_of_squared_distances.append(km.inertia_)

plt.plot(K, Sum_of_squared_distances, 'bx-')
plt.xlabel('k')
plt.ylabel('Sum_of_squared_distances')
plt.title('Elbow Method For Optimal k')
plt.show()

true_k = 4
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=200, n_init=10)
model.fit(X)
labels=model.labels_
wiki_cl=pd.DataFrame(list(zip(title,labels)),columns=['title','cluster'])
print(wiki_cl.sort_values(by=['cluster']))
