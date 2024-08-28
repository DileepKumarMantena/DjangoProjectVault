import requests

class CurrencyConverter:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = "https://v6.exchangerate-api.com/v6/{api_key}/latest/USD".format(api_key=self.api_key)

    def get_exchange_rates(self):
        response = requests.get(self.api_url)
        return response.json()

    def convert(self, amount, from_currency, to_currency):
        rates = self.get_exchange_rates()
        from_rate = rates['conversion_rates'].get(from_currency)
        to_rate = rates['conversion_rates'].get(to_currency)

        if from_rate and to_rate:
            base_amount = amount / from_rate
            return base_amount * to_rate
        return None
