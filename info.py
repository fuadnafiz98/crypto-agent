import requests

import json


def get_token_price(token_id, currency="usd"):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": token_id, "vs_currencies": currency}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Check for HTTP request errors
        data = response.json()
        price = data.get(token_id, {}).get(currency, None)
        if price is not None:
            return f"The price of {token_id} is {price} {currency.upper()}."
        else:
            return f"Unable to fetch the price for {token_id}."
    except Exception as e:
        return f"An error occurred: {e}"


# Example usage
token_id = "bitcoin"  # Replace with the token ID (e.g., ethereum, cardano)
currency = "usd"  # Replace with your desired currency


# Define the tool function
def coin_list_with_market_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {"vs_currency": "usd"}
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers, params=params)
    print(response.status_code)

    # Return top 5 coins with market data
    return json.dumps(response.json()[:5])


print(coin_list_with_market_data())
