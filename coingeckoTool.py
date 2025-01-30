import json
from phi.tools import Toolkit
from pycoingecko import CoinGeckoAPI

from dotenv import load_dotenv
import os

load_dotenv()


class CoinGeckoTools(Toolkit):
    def __init__(self, enable_all: bool = True):
        super().__init__(name="coingecko_tools")
        DEMO_API_KEY = os.environ["COINGECKO_DEMO_API_KEY"]
        self.cg = CoinGeckoAPI(demo_api_key=DEMO_API_KEY)

        if enable_all:
            # Register all methods
            self.register(self.get_current_coin_price)
            self.register(self.get_coin_info)
            self.register(self.get_coin_market_data)
            #            self.register(self.get_coin_historical_data)
            self.register(self.get_coin_tickers)
            self.register(self.get_coin_history)
            self.register(self.get_coin_status_updates)
            self.register(self.get_coin_ohlc)
            self.register(self.get_coin_categories_list)
            self.register(self.get_coin_categories)
            self.register(self.get_exchanges_list)
            self.register(self.get_exchange_info)
            self.register(self.get_exchange_tickers)
            self.register(self.get_exchange_volume_chart)
            self.register(self.get_finance_platforms)
            self.register(self.get_finance_products)
            self.register(self.get_indexes_list)
            self.register(self.get_index_info)
            self.register(self.get_derivatives_list)
            self.register(self.get_derivatives_exchanges_list)
            self.register(self.get_derivatives_exchange_info)
            self.register(self.get_status_updates)
            self.register(self.get_events)
            self.register(self.get_events_countries)
            self.register(self.get_events_types)
            self.register(self.get_global_data)
            self.register(self.get_global_defi_data)

    # Simple Endpoints
    def get_current_coin_price(self, coin_id: str, vs_currency: str = "usd") -> str:
        """
        Get the current price of a cryptocurrency.

        Args:
            coin_id (str): The CoinGecko ID of the cryptocurrency (e.g., "bitcoin").
            vs_currency (str): The currency to compare against (e.g., "usd", "eur"). Defaults to "usd".

        Returns:
            str: The current price of the cryptocurrency or an error message.
        """
        try:
            price = self.cg.get_price(ids=coin_id, vs_currencies=vs_currency)
            return f"{price[coin_id][vs_currency]:.4f} {vs_currency.upper()}"
        except Exception as e:
            return f"Error fetching current price for {coin_id}: {e}"

    # Coins Endpoints
    def get_coin_info(self, coin_id: str) -> str:
        """
        Get detailed information about a cryptocurrency.

        Args:
            coin_id (str): The CoinGecko ID of the cryptocurrency (e.g., "bitcoin").

        Returns:
            str: JSON containing detailed information about the cryptocurrency.
        """
        try:
            coin_info = self.cg.get_coin_by_id(coin_id)
            del coin_info["market_data"]
            del coin_info["developer_data"]

            return json.dumps(coin_info, indent=2)
        except Exception as e:
            return f"Error fetching info for {coin_id}: {e}"

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
            market_data = self.cg.get_coins_markets(
                id=coin_id, vs_currency=vs_currency, days=days
            )
            return json.dumps(market_data, indent=2)
        except Exception as e:
            return f"Error fetching market data for {coin_id}: {e}"

    def get_coin_tickers(self, coin_id: str) -> str:
        """
        Get tickers (exchange data) for a coin.

        Args:
            coin_id (str): The CoinGecko ID of the cryptocurrency (e.g., "bitcoin").

        Returns:
            str: JSON containing tickers for the cryptocurrency.
        """
        try:
            tickers = self.cg.get_coin_ticker_by_id(coin_id)
            return json.dumps(tickers, indent=2)
        except Exception as e:
            return f"Error fetching tickers for {coin_id}: {e}"

    def get_coin_history(self, coin_id: str, date: str) -> str:
        """
        Get historical data (e.g., price, market cap) for a coin on a specific date.

        Args:
            coin_id (str): The CoinGecko ID of the cryptocurrency (e.g., "bitcoin").
            date (str): The date in `dd-mm-yyyy` format.

        Returns:
            str: JSON containing historical data for the cryptocurrency.
        """
        try:
            history = self.cg.get_coin_history_by_id(coin_id, date)
            return json.dumps(history, indent=2)
        except Exception as e:
            return f"Error fetching history for {coin_id}: {e}"

    def get_coin_status_updates(self, coin_id: str) -> str:
        """
        Get status updates (e.g., development updates) for a coin.

        Args:
            coin_id (str): The CoinGecko ID of the cryptocurrency (e.g., "bitcoin").

        Returns:
            str: JSON containing status updates for the cryptocurrency.
        """
        try:
            status_updates = self.cg.get_coin_status_updates_by_id(coin_id)
            return json.dumps(status_updates, indent=2)
        except Exception as e:
            return f"Error fetching status updates for {coin_id}: {e}"

    def get_coin_ohlc(
        self, coin_id: str, vs_currency: str = "usd", days: int = 7
    ) -> str:
        """
        Get Open/High/Low/Close (OHLC) data for a coin.

        Args:
            coin_id (str): The CoinGecko ID of the cryptocurrency (e.g., "bitcoin").
            vs_currency (str): The currency to compare against (e.g., "usd", "eur"). Defaults to "usd".
            days (int): The number of days of OHLC data to retrieve. Defaults to 7.

        Returns:
            str: JSON containing OHLC data for the cryptocurrency.
        """
        try:
            ohlc = self.cg.get_coin_ohlc_by_id(
                coin_id, vs_currency=vs_currency, days=days
            )
            return json.dumps(ohlc, indent=2)
        except Exception as e:
            return f"Error fetching OHLC data for {coin_id}: {e}"

    # Categories Endpoints
    def get_coin_categories_list(self) -> str:
        """
        Get a list of all coin categories.

        Returns:
            str: JSON containing a list of all coin categories.
        """
        try:
            categories = self.cg.get_coins_categories_list()
            return json.dumps(categories, indent=2)
        except Exception as e:
            return f"Error fetching coin categories: {e}"

    def get_coin_categories(self) -> str:
        """
        Get market data for all coin categories.

        Returns:
            str: JSON containing market data for all coin categories.
        """
        try:
            categories = self.cg.get_coins_categories()
            return json.dumps(categories, indent=2)
        except Exception as e:
            return f"Error fetching coin categories market data: {e}"

    # Exchanges Endpoints
    def get_exchanges_list(self) -> str:
        """
        Get a list of all exchanges.

        Returns:
            str: JSON containing a list of all exchanges.
        """
        try:
            exchanges = self.cg.get_exchanges_list()
            return json.dumps(exchanges, indent=2)
        except Exception as e:
            return f"Error fetching exchanges list: {e}"

    def get_exchange_info(self, exchange_id: str) -> str:
        """
        Get detailed information about a specific exchange.

        Args:
            exchange_id (str): The ID of the exchange (e.g., "binance").

        Returns:
            str: JSON containing detailed information about the exchange.
        """
        try:
            exchange_info = self.cg.get_exchanges_by_id(exchange_id)
            return json.dumps(exchange_info, indent=2)
        except Exception as e:
            return f"Error fetching exchange info for {exchange_id}: {e}"

    def get_exchange_tickers(self, exchange_id: str) -> str:
        """
        Get tickers (trading pairs) for an exchange.

        Args:
            exchange_id (str): The ID of the exchange (e.g., "binance").

        Returns:
            str: JSON containing tickers for the exchange.
        """
        try:
            tickers = self.cg.get_exchanges_tickers_by_id(exchange_id)
            return json.dumps(tickers, indent=2)
        except Exception as e:
            return f"Error fetching tickers for {exchange_id}: {e}"

    def get_exchange_volume_chart(self, exchange_id: str, days: int = 7) -> str:
        """
        Get volume data for an exchange.

        Args:
            exchange_id (str): The ID of the exchange (e.g., "binance").
            days (int): The number of days of volume data to retrieve. Defaults to 7.

        Returns:
            str: JSON containing volume data for the exchange.
        """
        try:
            volume_chart = self.cg.get_exchanges_volume_chart_by_id(exchange_id, days)
            return json.dumps(volume_chart, indent=2)
        except Exception as e:
            return f"Error fetching volume chart for {exchange_id}: {e}"

    # Finance Endpoints
    def get_finance_platforms(self) -> str:
        """
        Get a list of decentralized finance (DeFi) platforms.

        Returns:
            str: JSON containing a list of DeFi platforms.
        """
        try:
            platforms = self.cg.get_finance_platforms()
            return json.dumps(platforms, indent=2)
        except Exception as e:
            return f"Error fetching finance platforms: {e}"

    def get_finance_products(self) -> str:
        """
        Get a list of DeFi products.

        Returns:
            str: JSON containing a list of DeFi products.
        """
        try:
            products = self.cg.get_finance_products()
            return json.dumps(products, indent=2)
        except Exception as e:
            return f"Error fetching finance products: {e}"

    # Indexes Endpoints
    def get_indexes_list(self) -> str:
        """
        Get a list of market indexes.

        Returns:
            str: JSON containing a list of market indexes.
        """
        try:
            indexes = self.cg.get_indexes()
            return json.dumps(indexes, indent=2)
        except Exception as e:
            return f"Error fetching indexes list: {e}"

    def get_index_info(self, market_id: str, index_id: str) -> str:
        """
        Get data for a specific market index.

        Args:
            market_id (str): The ID of the market (e.g., "binance").
            index_id (str): The ID of the index.

        Returns:
            str: JSON containing data for the market index.
        """
        try:
            index_info = self.cg.get_indexes_by_market_and_id(market_id, index_id)
            return json.dumps(index_info, indent=2)
        except Exception as e:
            return f"Error fetching index info for {market_id}/{index_id}: {e}"

    # Derivatives Endpoints
    def get_derivatives_list(self) -> str:
        """
        Get a list of derivatives (e.g., futures, options).

        Returns:
            str: JSON containing a list of derivatives.
        """
        try:
            derivatives = self.cg.get_derivatives()
            return json.dumps(derivatives, indent=2)
        except Exception as e:
            return f"Error fetching derivatives list: {e}"

    def get_derivatives_exchanges_list(self) -> str:
        """
        Get a list of derivative exchanges.

        Returns:
            str: JSON containing a list of derivative exchanges.
        """
        try:
            exchanges = self.cg.get_derivatives_exchanges()
            return json.dumps(exchanges, indent=2)
        except Exception as e:
            return f"Error fetching derivatives exchanges list: {e}"

    def get_derivatives_exchange_info(self, exchange_id: str) -> str:
        """
        Get data for a specific derivative exchange.

        Args:
            exchange_id (str): The ID of the derivative exchange.

        Returns:
            str: JSON containing data for the derivative exchange.
        """
        try:
            exchange_info = self.cg.get_derivatives_exchanges_by_id(exchange_id)
            return json.dumps(exchange_info, indent=2)
        except Exception as e:
            return f"Error fetching derivatives exchange info for {exchange_id}: {e}"

    # Status Updates Endpoints
    def get_status_updates(self) -> str:
        """
        Get global status updates (e.g., system updates).

        Returns:
            str: JSON containing global status updates.
        """
        try:
            status_updates = self.cg.get_status_updates()
            return json.dumps(status_updates, indent=2)
        except Exception as e:
            return f"Error fetching status updates: {e}"

    # Events Endpoints
    def get_events(self) -> str:
        """
        Get global events (e.g., conferences, meetups).

        Returns:
            str: JSON containing global events.
        """
        try:
            events = self.cg.get_events()
            return json.dumps(events, indent=2)
        except Exception as e:
            return f"Error fetching events: {e}"

    def get_events_countries(self) -> str:
        """
        Get a list of countries with events.

        Returns:
            str: JSON containing a list of countries with events.
        """
        try:
            countries = self.cg.get_events_countries()
            return json.dumps(countries, indent=2)
        except Exception as e:
            return f"Error fetching events countries: {e}"

    def get_events_types(self) -> str:
        """
        Get a list of event types.

        Returns:
            str: JSON containing a list of event types.
        """
        try:
            types = self.cg.get_events_types()
            return json.dumps(types, indent=2)
        except Exception as e:
            return f"Error fetching events types: {e}"

    # Global Endpoints
    def get_global_data(self) -> str:
        """
        Get global cryptocurrency data (e.g., total market cap, total volume).

        Returns:
            str: JSON containing global cryptocurrency data.
        """
        try:
            global_data = self.cg.get_global()
            return json.dumps(global_data, indent=2)
        except Exception as e:
            return f"Error fetching global data: {e}"

    def get_global_defi_data(self) -> str:
        """
        Get global DeFi data.

        Returns:
            str: JSON containing global DeFi data.
        """
        try:
            defi_data = self.cg.get_global_decentralized_finance_defi()
            return json.dumps(defi_data, indent=2)
        except Exception as e:
            return f"Error fetching global DeFi data: {e}"
