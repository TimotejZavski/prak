
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

# Load JSON data into a DataFrame
with open('uploads/output.json', 'r') as file:
    data = json.load(file)

# Create a DataFrame from JSON data
df = pd.DataFrame(data)

# Extract temperatures and elevation information
df['January Avg. High (°C)'] = df['January(Avg. high °C (°F))'].apply(lambda x: float(x.split(' ')[0]))
df['July Avg. High (°C)'] = df['July(Avg. high °C (°F))'].apply(lambda x: float(x.split(' ')[0]))
df['Annual Avg. High (°C)'] = df['Annual(Avg. high °C (°F))'].apply(lambda x: float(x.split(' ')[0]))
df['Elevation (m)'] = df['Elevation'].apply(lambda x: float(x.split('m')[0].strip()))

# Set the color palette for monochrome blue
sns.set_palette(sns.color_palette("Blues"))

# Create directory for saving images if it doesn't exist
image_dir = '/Users/timzav/Desktop/prak/static/images'
os.makedirs(image_dir, exist_ok=True)

# Plot January Average High Temperature
plt.figure(figsize=(24, 13.5))
sns.barplot(x='Community', y='January Avg. High (°C)', data=df)
plt.title('January Average High Temperature (°C)')
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig(f'{image_dir}/january_avg_high_temp.png')

# Plot July Average High Temperature
plt.figure(figsize=(24, 13.5))
sns.barplot(x='Community', y='July Avg. High (°C)', data=df)
plt.title('July Average High Temperature (°C)')
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig(f'{image_dir}/july_avg_high_temp.png')

# Plot Annual Average High Temperature
plt.figure(figsize=(24, 13.5))
sns.barplot(x='Community', y='Annual Avg. High (°C)', data=df)
plt.title('Annual Average High Temperature (°C)')
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig(f'{image_dir}/annual_avg_high_temp.png')
