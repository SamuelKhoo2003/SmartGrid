# This API Endpoint has since been deprecated and is no longer in use. The code is kept for reference purposes.

import requests
import json
import time
import random

class WebEnergyUsageTester:
    def __init__(self):
        self.day = 1

    def call_api(self):
        # Making the HTTP request to the web link
        response = requests.get("https://icelec50015.azurewebsites.net/yesterday")

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON data
            data = response.json()
            # Calculate the sum of all the demand values
            total_demand = sum(entry['demand'] for entry in data)
            print("Total demand:", total_demand)

            # Performing the API post with the extracted information
            post_data = {"dayID": self.day, "energyUsed": total_demand}
            response = requests.post("https://evuc3y0h1g.execute-api.eu-north-1.amazonaws.com/PROD/accessUsageLog", json=post_data)
            print("Successful post") if response.status_code == 200 else print("Failed post")
        else:
            print("Failed to retrieve data from the web link.")

    def run_api_calls(self):
        while True:
            self.call_api()
            self.day += 1
            time.sleep(300)  # Sleep for 5 minutes (300 seconds)

class LocalEnergyUsageTester:
    def __init__(self):
        self.url = "https://evuc3y0h1g.execute-api.eu-north-1.amazonaws.com/PROD/accessUsageLog"

    def generate_random_data(self, inputval):
        day = inputval
        energyUsed = round(random.uniform(70, 102), 2)
        return day, energyUsed

    def test_api_post(self, day, energyUsed):
        data = {
            "dayID": day,
            "energyUsed": energyUsed
        }
        response = requests.post(self.url, json=data)
        print("Successful post") if response.status_code == 200 else print("Failed post")

    def run(self):
        inputval = int(input("Enter a starting day: "))
        while True:
            inputval += 1
            day, energyUsed = self.generate_random_data(inputval)
            self.test_api_post(day, energyUsed)
            time.sleep(5)


if __name__ == "__main__":
    # this is for the true energy from the API calls
    # web_tester = WebEnergyUsageTester()
    # web_tester.run_api_calls()

    local_tester = LocalEnergyUsageTester()
    local_tester.run()

