import requests
import time
import unittest

class TestLimitOrderTesting(unittest.TestCase):
    def test_performance(self):
        start_time = time.time()

        # Code to pull all values, sort them, and take the most recent 90 values
        url = "https://evuc3y0h1g.execute-api.eu-north-1.amazonaws.com/PROD/accessEnergyLog"
        response = requests.get(url)
        data = response.json()
        sorted_data = sorted(data, key=lambda entry: entry['dayID'], reverse=True)
        recent_values = sorted_data[:90]

        end_time = time.time()
        execution_time = end_time - start_time
        print(sorted_data)
        print(f"Execution time: {execution_time} seconds")


# class DataRetriever:
#     def __init__(self, url):
#         self.url = url

#     def get_order_of_days(self):
#         response = requests.get(self.url)
#         data = response.json()
#         order_of_days = [entry['dayID'] for entry in data]
#         return order_of_days

#     def get_num_elements(self):
#         response = requests.get(self.url)
#         data = response.json()
#         num_elements = len(data)
#         return num_elements


# data_retriever = DataRetriever("https://evuc3y0h1g.execute-api.eu-north-1.amazonaws.com/PROD/accessEnergyLog")

# order_of_days = data_retriever.get_order_of_days()
# print(order_of_days)

# num_elements = data_retriever.get_num_elements()
# print(f"Number of elements returned: {num_elements}")

if __name__ == '__main__':
    unittest.main()
    pass
