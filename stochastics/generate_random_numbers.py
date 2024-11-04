import pygame
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

pygame.init()

screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Draw with Red Line and Get Coordinates")

white = (255, 255, 255)
red = (255, 0, 0)

drawing = False
coordinates = []
screen.fill(white)

# Flag to indicate when to exit the main loop
running = True

# Main loop for Pygame drawing
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            coordinates = [event.pos]
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                pos = event.pos
                coordinates.append(pos)
                if len(coordinates) > 1:
                    pygame.draw.line(screen, red, coordinates[-2], coordinates[-1], 3)
    pygame.display.flip()

pygame.quit()

# Extract x and y values from the coordinates
x_values = [coord[0] for coord in coordinates]
y_values = [coord[1] for coord in coordinates]

# Normalize x values to start from 0 for better integration results
x_values = np.array(x_values) - min(x_values)

area = np.trapz(y_values, x_values)
print("Area before normalization:", area)
normalized_pdf_values = y_values / area
normalized_area = np.trapz(normalized_pdf_values, x_values)
print("Area after normalization:", normalized_area)

# Compute the cumulative sum to get the CDF
cdf_values = np.cumsum(normalized_pdf_values)
cdf_values /= cdf_values[-1]

# Set up the initial number of samples
initial_num_samples = 1000

# Function to generate samples using inverse transform sampling
def generate_samples(num_samples):
    uniform_random_values = np.random.uniform(0, 1, num_samples)
    return np.interp(uniform_random_values, cdf_values, x_values)

# Create the initial plot
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.25)
generated_samples = generate_samples(initial_num_samples)
hist_plot = ax.hist(generated_samples, bins=30, density=True, alpha=0.6, color='b', label="Generated samples")
ax.plot(x_values, normalized_pdf_values, 'r-', lw=2, label="Original PDF")
ax.set_xlabel('x')
ax.set_ylabel('Probability Density')
ax.set_title('Generated Samples with Adjustable Count')
ax.legend()

# Set up the slider
ax_slider = plt.axes([0.1, 0.1, 0.8, 0.03], facecolor='lightgoldenrodyellow')
sample_slider = Slider(ax_slider, 'Number of Samples', 10, 10000, valinit=initial_num_samples, valstep=100)

# Update function for the slider
def update(val):
    num_samples = int(sample_slider.val)
    ax.clear()  # Clear the previous histogram
    # Regenerate samples and plot
    new_samples = generate_samples(num_samples)
    ax.hist(new_samples, bins=30, density=True, alpha=0.6, color='b', label="Generated samples")
    ax.plot(x_values, normalized_pdf_values, 'r-', lw=2, label="Original PDF")
    ax.set_xlabel('x')
    ax.set_ylabel('Probability Density')
    ax.set_title('Generated Samples with Adjustable Count')
    ax.legend()
    fig.canvas.draw_idle()

# Attach the update function to the slider
sample_slider.on_changed(update)

plt.show()

