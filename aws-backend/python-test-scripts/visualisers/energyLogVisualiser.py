import requests
from tabulate import tabulate

# I want to tabulate the data and display it as well as plot a graph of the json data given
import matplotlib.pyplot as plt

# Make the API call
response = requests.get('https://evuc3y0h1g.execute-api.eu-north-1.amazonaws.com/PROD/accessEnergyLog')
if response.status_code != 200:
    print('Error:', response.status_code)
    exit()

# Extract the values from the API response
data = response.json()
data.sort(key=lambda item: item['dayID'])
x_values = [item['dayID'] for item in data]
energyProduced = [item['energyProduced'] for item in data]
energyUsed = [item['energyUsed'] for item in data]

# Plot the graph
plt.plot(x_values, energyUsed, label='Energy Used')
plt.xlabel('Day')
plt.ylabel('Energy Used')
plt.title('Day VS Energy Used')
plt.legend()
plt.show()

# Create a list of rows for the table
table_data = []
for item in data:
    table_data.append([item['dayID'], item['energyProduced'], item['energyUsed']])

# Display the table in the terminal
print(tabulate(table_data, headers=['Day', 'Energy Produced', 'Energy Used']))

# Plot the graph
plt.plot(x_values, energyProduced, label='Energy Produced')
plt.xlabel('Day')
plt.ylabel('Energy Produced')
plt.title('Day VS Energy Produced')
plt.legend()
plt.show()

# # Create a list of rows for the table
# table_data = []
# for item in data:
#     table_data.append([item['dayID'], item['energyProduced']])

# # Display the table in the terminal
# print(tabulate(table_data, headers=['Day', 'Energy Produced']))