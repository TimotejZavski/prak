
import matplotlib.pyplot as plt
import json

# Load the data
with open('uploads/output.json', 'r') as f:
    data = json.load(f)

# Extract the relevant data for the latency comparisons
models = [model_data['Model'] for model_data in data]
latencies_ane = [float(model_data['Latency ANE']) for model_data in data]
latencies_gpu = [float(model_data['Latency GPU']) for model_data in data]
latencies_cpu = [float(model_data['Latency CPU']) for model_data in data]

# Configure monochrome blue palette using hex codes
colors = ['#08306b', '#08519c', '#2171b5', '#4292c6', '#6baed6', '#9ecae1', '#c6dbef']

fig, ax = plt.subplots()

# Ensure that each model uses a different shade of blue
num_models = len(models)
color_index_step = len(colors) // num_models
selected_colors = colors[::color_index_step][:num_models]

# Create bar chart
bar_width = 0.2
index = range(num_models)

# Plot each latency on the same chart with different colors
bars1 = ax.bar(index, latencies_ane, bar_width, color=selected_colors[0], label='Latency ANE')
bars2 = ax.bar([i + bar_width for i in index], latencies_gpu, bar_width, color=selected_colors[1], label='Latency GPU')
bars3 = ax.bar([i + 2*bar_width for i in index], latencies_cpu, bar_width, color=selected_colors[2], label='Latency CPU')

# Labeling and Formatting
plt.xlabel('Model')
plt.ylabel('Latency (seconds)')
plt.title('Latency Comparison for each model')
plt.xticks([i + bar_width for i in range(num_models)], models, rotation=45, ha='right')
plt.legend()

# Adjust layout for better fit
plt.tight_layout()

# Save the figure
plt.savefig('/Users/timzav/Desktop/prak/static/images/latency_comparison.png', dpi=300)
