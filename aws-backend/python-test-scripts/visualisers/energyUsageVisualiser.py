# This API Endpoint has since been deprecated and is no longer in use. The code is kept for reference purposes.

import requests
from tabulate import tabulate

import matplotlib.pyplot as plt

response = requests.get('https://evuc3y0h1g.execute-api.eu-north-1.amazonaws.com/PROD/accessUsageLog')
if response.status_code != 200:
    print('Error: ', response.status_code)
    exit()

data = response.json()
data.sort(key=lambda item: item['dayID'])
day = [item['dayID'] for item in data]
usage = [item['energyUsed'] for item in data]

plt.plot(day, usage, label='Energy Used')
plt.xlabel('Day')
plt.ylabel('Energy Used')
plt.title('Day VS Energy Used')
plt.legend()
plt.show()

table_data = []
for item in data:
    table_data.append([item['dayID'], item['energyUsed']])

print(tabulate(table_data, headers=['Day', 'Energy Used']))