import unittest
import requests

class TestAllLog(unittest.TestCase):
    def test_get_trade_log(self):
        response = requests.get('https://evuc3y0h1g.execute-api.eu-north-1.amazonaws.com/PROD/accessTradeLog')

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertTrue(any('dayID' in d and 'earnings' in d and 'energySold' in d and 'energyBought' in d for d in data))

    # def test_get_usage_log(self):
    #     response = requests.get('https://evuc3y0h1g.execute-api.eu-north-1.amazonaws.com/PROD/accessUsageLog')

    #     self.assertEqual(response.status_code, 200)

    #     data = response.json()
    #     self.assertTrue(any('energyUsed' in d for d in data))

    def test_get_energy_log(self):
        response = requests.get('https://evuc3y0h1g.execute-api.eu-north-1.amazonaws.com/PROD/accessEnergyLog')

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertTrue(any('energyUsed' in d and 'energyProduced' in d for d in data))


if __name__ == '__main__':
    # Create a test suite
    suite = unittest.TestSuite()

    # Add test cases to the suite
    suite.addTest(TestAllLog('test_get_trade_log'))
    suite.addTest(TestAllLog('test_get_usage_log'))
    suite.addTest(TestAllLog('test_get_energy_log'))

    # Run all test cases
    unittest.TextTestRunner().run(suite)