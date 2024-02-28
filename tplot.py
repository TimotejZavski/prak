
import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Custom monochrome blue color palette
cmap = LinearSegmentedColormap.from_list('monoblue', ['lightblue', 'mediumblue', 'darkblue'], N=256)

# Load the data from the JSON file
with open('uploads/output.json', 'r') as f:
    data = json.load(f)

# Convert the data to a pandas DataFrame
df = pd.DataFrame(data)

# Drop rows with missing 'sex' column
df = df.dropna(subset=['sex'])

# Convert numeric columns to the correct data type
numeric_columns = ['\ufeffculmen_length_mm', 'culmen_depth_mm', 'flipper_length_mm', 'body_mass_g']
df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric)

# Plot 1: Culmen length vs. Culmen depth
plt.figure(figsize=(1920/96, 1080/96), dpi=96)  # Set figure size to 1920x1080
plt.scatter(df['\ufeffculmen_length_mm'], df['culmen_depth_mm'], c=df['culmen_depth_mm'], cmap=cmap)
plt.xlabel('Culmen Length (mm)')
plt.ylabel('Culmen Depth (mm)')
plt.title('Culmen Length vs Culmen Depth')
plt.colorbar(label='Culmen Depth (mm)')
plt.savefig('/Users/timzav/Desktop/prak/static/images/culmen_length_vs_depth.png')
plt.close()

# Plot 2: Flipper length vs. Body mass
plt.figure(figsize=(1920/96, 1080/96), dpi=96)  # Set figure size to 1920x1080
plt.scatter(df['flipper_length_mm'], df['body_mass_g'], c=df['body_mass_g'], cmap=cmap)
plt.xlabel('Flipper Length (mm)')
plt.ylabel('Body Mass (g)')
plt.title('Flipper Length vs Body Mass')
plt.colorbar(label='Body Mass (g)')
plt.savefig('/Users/timzav/Desktop/prak/static/images/flipper_length_vs_body_mass.png')
plt.close()
