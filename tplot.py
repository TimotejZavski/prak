
import json
import matplotlib.pyplot as plt
import numpy as np

# Load data from JSON file
with open('/Users/timzav/Desktop/prak/uploads/output.json', 'r') as f:
    data = json.load(f)

# Extract x and y values for the chart
x_values = np.array([d['culmen_length_mm'] for d in data if d['sex'] != ''])
y_values = np.array([d['flipper_length_mm'] for d in data if d['sex'] != ''])
sexes = [d['sex'].lower() for d in data if d['sex'] != '']

# Create a new figure with specified size
fig, ax = plt.subplots(figsize=(1920/100, 1080/100))

# Create a boxplot
bp = ax.boxplot(y_values, vert=False, whis=[5, 95], showfliers=False)

# Set plot title and labels
ax.set_title('Penguin Flipper Length by Culmen Length')
ax.set_xlabel('Culmen Length (mm)')
ax.set_ylabel('Flipper Length (mm)')

# Set color palette
monochrome_blue = ['#9fc5e8', '#64a9ce', '#3b8dd0']
for i, b in enumerate(bp['boxes']):
    b.set_facecolor(monochrome_blue[int(sexes[i] == 'male')])

# Save plot to file
plt.savefig('/Users/timzav/Desktop/prak/static/images/boxplot.png', dpi=100)
