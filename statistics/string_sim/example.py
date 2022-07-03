from scipy.spatial import distance

# Example 1:
# Strings:

#string1 = 'YNNNYNNNNNNNNNNNNYNNNNNN'
string1 = 'YNNNYNNNNNNNNNNNNYYYYYYY'
string2 = 'NNNNNNNNNNNNNNNNNYYYYYYY'

# Normalized Hamming Distance

Normalized_HD = distance.hamming(list(string1), list(string2))
print('The Normalized Hamming Distance between {} and {} is {}.'.format(string1, string2, Normalized_HD))

# Original Hamming Distance
print('The Hamming Distance between {} and {} is {}'. format(string1, string2, Normalized_HD*len(string1)))

