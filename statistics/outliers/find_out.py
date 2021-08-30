import numpy as np
from scipy import stats

def remove_outliers(data):
    a = np.array(data)
    upper_quartile = np.percentile(a, 75, interpolation = 'midpoint')
    lower_quartile = np.percentile(a, 25, interpolation = 'midpoint')
    iqr = stats.iqr(data, interpolation = 'midpoint')
    quartileset = (lower_quartile - iqr, upper_quartile + iqr)
    resultlist = []
    outliers = []
    for y in a.tolist():
        if y >= quartileset[0] and y <= quartileset[1]:
            resultlist.append(y)
        else:
            outliers.append(y)
    return resultlist,outliers

x = [3,10,14,19,22,29,32,36,49,70]

result_list,outliers = remove_outliers(x)
print(result_list)
print(outliers)
