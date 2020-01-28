import numpy as np
from numpy import sqrt
from numpy.testing import assert_allclose
import scipy.special as sc
import scipy.special.orthogonal as orth

rf = lambda a, b: lambda n, mu: sc.roots_jacobi(n, a, b, mu)
ef = lambda a, b: lambda n, x: orth.eval_jacobi(n, a, b, x)

rtol=1e-15
atol=1e-14
N= 25

root_func = rf(18.24, 27.3)
eval_func = ef(18.24, 27.3)
x, w, mu = root_func(N, True)

# test orthogonality. Note that the results need to be normalized,
# otherwise the huge values that can arise from fast growing
# functions like Laguerre can be very confusing.

n = np.arange(N)
v = eval_func(n[:,np.newaxis], x)
vv = np.dot(v*w, v.T)
vd = 1 / np.sqrt(vv.diagonal())
vv = vd[:, np.newaxis] * vv * vd
assert_allclose(vv, np.eye(N), rtol, atol)
