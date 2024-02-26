
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data from JSON file
df = pd.read_json('uploads/output.json')

# Set color palette to monochrome blue
blue_pal = sns.color_palette("Blues")

# Scatter plot of culmen_length_mm vs culmen_depth_mm
plt.figure(figsize=(19.20, 10.80))
sns.scatterplot(data=df, x='﻿culmen_length_mm', y='culmen_depth_mm', palette=blue_pal)
plt.savefig('/Users/timzav/Desktop/prak/static/images/scatter_culmen.png')

# Histogram of body_mass_g
plt.figure(figsize=(19.20, 10.80))
sns.histplot(data=df, x='body_mass_g', color=blue_pal[3], bins=30)
plt.savefig('/Users/timzav/Desktop/prak/static/images/histogram_body_mass.png')
