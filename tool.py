from pycoingecko import CoinGeckoAPI
import json

from dotenv import load_dotenv
import os

load_dotenv()


class CoinGecko:
    def __init__(self, enable_all: bool = True):
        DEMO_API_KEY = os.environ["COINGECKO_DEMO_API_KEY"]
        self.cg = CoinGeckoAPI(demo_api_key=DEMO_API_KEY)

    def get_coin_market_data(
        self, coin_id: str, vs_currency: str = "usd", days: str = "30"
    ) -> str:
        """
        Get historical market data (price, market cap, volume) for a coin.
        Also use to get the market cap or market capacity, volume etc

        Args:
            coin_id (str): The CoinGecko ID of the cryptocurrency (e.g., "bitcoin").
            vs_currency (str): The currency to compare against (e.g., "usd", "eur"). Defaults to "usd".
            days (str): The number of days of historical data to retrieve. Defaults to "30".

        Returns:
            str: JSON containing historical market data for the cryptocurrency.
        """
        try:
            market_data = self.cg.get_coin_by_id(
                id=coin_id, vs_currency=vs_currency, days=days
            )
            return json.dumps(market_data, indent=2)
        except Exception as e:
            return f"Error fetching market data for {coin_id}: {e}"


c = CoinGecko()
print(c.get_coin_market_data("bitcoin"))
