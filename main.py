from phi.agent import Agent
from phi.model.openai import OpenAIChat
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Define the tool function
def coin_list_with_market_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {"vs_currency": "usd"}
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers, params=params)
    print(response.status_code)
    if response.status_code == 200:
        # Return top 5 coins with market data
        return json.dumps(response.json()[:5])
    return ""


def get_pepe_id():
    """Use this function to get the token id.

    Args:
        token_id (str): the id of the token

    Returns:
        str: JSON string of the token id,
    """

    return "american-pepe"


def get_bitcoin_id():
    """Use this function to get the token id.

    Args:
        token_id (str): the id of the token

    Returns:
        str: JSON string of the token id,
    """

    return "bitcoin"


def get_token_price(token_id="", currency="usd"):
    print(token_id)
    """Use this function to get the currency of a token.

    Args:
        token_id (str): the id of the token. The token_id is passed by the agent

    Returns:
        str: JSON string of the token price.
    """

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


# Create the agent
crypto_agent = Agent(
    name="crypto-agent",
    model=OpenAIChat(id="gpt-4o-mini"),  # Specify model ID
    tools=[get_bitcoin_id, get_pepe_id, get_token_price],  # Register tools
    # tool_choice={
    #    "type": "function",
    #    "function": {"name": "coin_list_with_market_data"},
    # },  # Let the agent decide on tool usage
    show_tool_calls=True,
    instructions=[
        "You are an expert in cryptocurrency with a deep understanding of cryptocurrency markets.",
        "You should take the id from the functions and pass it to get_token_price() to get the actual value",
    ],
    markdown=True,
)

# Test the agent with a query
response = crypto_agent.print_response(
    #   "What is the best coin to invest in at this moment, and which market should I target?"
    # "What is the price of Pepe?"
    # "What is the price of SUI?"
    "What is the price of Pepe"
)
