python
import json
import matplotlib.pyplot as plt

# Read the JSON file
with open('uploads/output.json') as file:
    data = json.load(file)

# Extract the price and property square footage from the data
prices = [int(item['PRICE']) for item in data]
sqft = [int(item['PROPERTYSQFT']) for item in data]

# Create the scatter plot
plt.figure(figsize=(8, 6))
plt.scatter(sqft, prices)
plt.xlabel('Property Square Footage')
plt.ylabel('Price')
plt.title('Price vs. Property Square Footage')

# Save the plot as a PNG image
plt.savefig('/Users/timzav/Desktop/prak/static/images/price_vs_sqft.png')
plt.close()
