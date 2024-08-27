import requests
from tabulate import tabulate

# I want to tabulate the data and display it as well as plot a graph of the json data given
import matplotlib.pyplot as plt

# Make the API call
response = requests.get('https://evuc3y0h1g.execute-api.eu-north-1.amazonaws.com/PROD/accessTradeLog')
if response.status_code != 200:
    print('Error:', response.status_code)
    exit()
# print(response.status_code)

# Extract the values from the API response
data = response.json()
data.sort(key=lambda item: item['dayID'])
day = [item['dayID'] for item in data]
earnings = [item['earnings'] for item in data]
energy_bought = [item['energyBought'] for item in data]
energy_sold = [item['energySold'] for item in data]

# Plot the graph
plt.plot(day, earnings, label='Earnings')
plt.xlabel('Day')
plt.ylabel('Earnings')
plt.title('Day VS Earnings')
plt.legend()
plt.show()

# Create a bar chart of day with energy bought and sold
plt.bar(day, energy_bought, label='Energy Bought')
plt.bar(day, energy_sold, label='Energy Sold')
plt.xlabel('Day')
plt.ylabel('Energy')
plt.title('Day VS Energy Bought and Sold')
plt.legend()
plt.show()

# # Create a list of rows for the table
table_data = []
for item in data:
    table_data.append([item['dayID'], item['earnings'], item['energyBought'], item['energySold']])

# Display the table in the terminal
print(tabulate(table_data, headers=['Day', 'Earnings', 'Energy Bought', 'Energy Sold']))