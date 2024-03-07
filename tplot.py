
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json

# Load the data from the JSON file
json_file_path = 'uploads/output.json'
with open(json_file_path, 'r') as f:
    data = json.load(f)

# Create a DataFrame from the loaded data
df = pd.DataFrame(data)

# Ensure proper data types
df['Age'] = df['Age'].astype(int)
df['Height'] = df['Height'].astype(float)
df['Weight'] = df['Weight'].astype(float)
df['BMI'] = df['BMI'].astype(float)
df['PhysicalActivityLevel'] = df['PhysicalActivityLevel'].astype(int)

# Chart 1: Distribution of Obesity Categories
plt.figure(figsize=(10, 6))
obesity_counts = df['ObesityCategory'].value_counts()
sns.barplot(x=obesity_counts.index, y=obesity_counts.values)
plt.title("Distribution of Obesity Categories")
plt.xlabel('Obesity Category')
plt.ylabel('Count')
plt.savefig('/Users/timzav/Desktop/prak/static/images/obesity_distribution.png', dpi=300)

# Chart 2: Box plot of BMI by Physical Activity Level
plt.figure(figsize=(12, 7))
sns.boxplot(x='PhysicalActivityLevel', y='BMI', data=df)
plt.title('BMI by Physical Activity Level')
plt.xlabel('Physical Activity Level')
plt.ylabel('BMI')
plt.savefig('/Users/timzav/Desktop/prak/static/images/bmi_by_activity.png', dpi=300)
