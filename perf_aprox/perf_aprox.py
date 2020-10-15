import matplotlib.pyplot as plt
import numpy as np

m = 2
b = 1

x = np.linspace(-5,5,100)
y = (m*x)+b

label_str = 'y=%sx+%s' % (m,b)

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
x = np.linspace(-5,5,100)
ax.spines['left'].set_position('center')
ax.spines['bottom'].set_position('center')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

plt.plot(x, y, '-r', label=label_str)
plt.title('Graph of ' + label_str)
plt.legend(loc='upper left')
plt.grid()
plt.show()

