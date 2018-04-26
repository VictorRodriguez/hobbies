import numpy as np
import warnings

print("np.version.version")
print(np.version.version)

warnings.simplefilter("always", category=RuntimeWarning)
print(np.min(np.full((7,), np.nan, dtype=np.float64)))
print(np.min(np.full((8,), np.nan, dtype=np.float64)))

print(np.min([1.0, 2.0, np.nan]))
print(np.min([1.0, np.nan, 2.0]))
print(np.min([np.nan, 1.0, 2.0]))
print(np.min([np.nan, 1.0]))
