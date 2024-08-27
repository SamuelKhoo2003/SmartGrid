import requests
import time
import random

class TradeLogTester:
    def __init__(self):
        self.url = "https://evuc3y0h1g.execute-api.eu-north-1.amazonaws.com/PROD/accessTradeLog"

    def generate_random_data(self, inputval):
        day = inputval
        earnings = round(random.uniform(0, -500), 2)
        energysold = round(random.uniform(0, 198), 2)
        energybought = round(random.uniform(0, 198), 2)
        return day, earnings, energysold, energybought

    def test_api_post(self, day, earnings, energysold, energybought):
        data = {
            "dayID": day,
            "earnings": earnings,
            "energySold": energysold,
            "energyBought": energybought
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
            day, earnings, energysold, energybought = self.generate_random_data(inputval)
            self.test_api_post(day, earnings, energysold, energybought)
            time.sleep(2)

if __name__ == "__main__":
    tester = TradeLogTester()
    tester.run()

# CORE Problem: If the primary key remains the same then it is troublesome to update the data.
# This might be a problem we may face down the future? What primary key to use if we want to update the data? (Way easier to do local computer time stamp as primary key)
# Might consider this or we would have to carry over the date from the 3rd party web server to our own computer and then update the data.