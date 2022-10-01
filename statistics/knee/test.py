from kneed import DataGenerator, KneeLocator
import matplotlib.pyplot as plt


x, y = DataGenerator.figure2()

print([round(i, 3) for i in x])
print([round(i, 3) for i in y])

# plot
fig, ax = plt.subplots()

ax.plot(x, y, linewidth=2.0)
plt.show()

kneedle = KneeLocator(x, y)

print(round(kneedle.knee, 3))

print(round(kneedle.elbow, 3))

kneedle.plot_knee()

plt.show()
