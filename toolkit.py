from phi.tools import Toolkit
from dotenv import load_dotenv
from pycoingecko import CoinGeckoAPI
import os

load_dotenv()


class CoinGeckoToolkit(Toolkit):
    def __init__(self):
        super().__init__(name="Coingecko Toolkit")
        DEMO_API_KEY = os.environ["COINGECKO_DEMO_API_KEY"]
        self.cg = CoinGeckoAPI(demo_api_key=DEMO_API_KEY)
        self.register(self.get_token_price)

    def get_token_price(self, id: str, currency: str = "usd") -> str:
        """Use this function to get the price of a token in a specific currency.

        Args:
            id (str): The id of the token. This is passed by the Agent.
            currency (str): The currency to fetch the price in. Default is 'usd'.

        Returns:
            str: The price of the token in the specified currency.
        """
        try:
            data = self.cg.get_price(ids=id, vs_currencies=currency)
            price = data.get(id, {}).get(currency, None)

            if price is not None:
                return f"The price of {id} is {price} {currency.upper()}."
            else:
                return f"Unable to fetch the price for {id}."
        except Exception as e:
            return f"An error occurred: {e}"


#        url = "https://api.coingecko.com/api/v3/simple/price"
#        params = {"ids": id, "vs_currencies": currency}

#        try:
#            response = requests.get(url, params=params)
#            response.raise_for_status()
#            data = response.json()
#            price = data.get(id, {}).get(currency, None)
#            if price is not None:
#                return f"The price of {id} is {price} {currency.upper()}."
#            else:
#                return f"Unable to fetch the price for {id}."
#        except Exception as e:
#            return f"An error occurred: {e}"
