
import json
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load data from JSON file
with open('uploads/output.json') as f:
    data = json.load(f)

# Extract sex column and create separate lists for male and female data
males = [dict[k] for k, d in data for d in (dict,) if d['sex'] == 'MALE']
females = [d for d in data if d['sex'] == 'FEMALE']

# Create subplots
fig, axs = plt.subplots(1, 2, figsize=(20, 10))

# Plot histogram of culmen length for males and females
sns.histplot(data=males, x='culmen_length_mm', ax=axs[0], color='blue')
sns.histplot(data=females, x='culmen_length_mm', ax=axs[0], color='lightblue')
axs[0].set_title('Culmen Length (mm) by Sex')

# Plot histogram of flipper length for males and females
sns.histplot(data=males, x='flipper_length_mm', ax=axs[1], color='blue')
sns.histplot(data=females, x='flipper_length_mm', ax=axs[1], color='lightblue')
axs[1].set_title('Flipper Length (mm) by Sex')

# Save plot as PNG image with high resolution
plt.savefig('/Users/timzav/Desktop/prak/static/images/chart.png', dpi=300, bbox_inches='tight')
plt.close()
