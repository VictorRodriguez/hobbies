from sklearn.metrics.cluster import adjusted_rand_score
from sklearn.metrics.cluster import normalized_mutual_info_score
from sklearn.metrics.cluster import fowlkes_mallows_score

import pandas as pd

df = pd.read_csv("clusters_spec2017.csv")
labels_true = df["REAL"].tolist()

df = pd.read_csv("clusters.csv")
labels_pred = df["PRED"].tolist()

df = pd.DataFrame(list(zip(labels_true, labels_true, df["test_name"].tolist())),
                  columns=['labels_true', 'labels_pred', 'test_name'])
print(df)

result = adjusted_rand_score(labels_true, labels_pred)
print("\nadjusted_rand_score")
print(result)

result = normalized_mutual_info_score(labels_true, labels_pred)
print("\nnormalized_mutual_info_score")
print(result)

result = fowlkes_mallows_score(labels_true, labels_pred)
print("\nfowlkes_mallows_score")
print(result)
