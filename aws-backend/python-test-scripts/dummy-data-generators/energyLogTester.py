import requests
import time
import random

class EnergyLogTester:
    def __init__(self):
        self.url = "https://evuc3y0h1g.execute-api.eu-north-1.amazonaws.com/PROD/accessEnergyLog"

    def generate_random_data(self, inputval):
        day = inputval
        energyUsed = round(random.uniform(0, 1), 2)
        energyProduced = round(random.uniform(0, 198), 2)
        return day, energyUsed, energyProduced

    def test_api_post(self, day, energyUsed, energyProduced):
        data = {
            "dayID": day,
            "energyUsed": energyUsed,
            "energyProduced": energyProduced
        }

        try:
            response = requests.post(self.url, json=data)
            response.raise_for_status()  # Raise an exception if the request was unsuccessful
            print("POST request successful!")
        except requests.exceptions.RequestException as e:
            print("POST request failed:", e)

    def run(self):
        inputval = int(input("Enter a starting day: "))
        while True:
            inputval += 1
            day, energyUsed, energyProduced = self.generate_random_data(inputval)
            self.test_api_post(day, energyUsed, energyProduced)
            time.sleep(2)

if __name__ == "__main__":
    tester = EnergyLogTester()
    tester.run()