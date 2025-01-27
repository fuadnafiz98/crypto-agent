from phi.agent import Agent
from phi.model.openai import OpenAIChat
import requests
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()


# Define the tool function
def coin_list_with_market_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {"vs_currency": "usd"}
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers, params=params)

    # Return top 5 coins with market data
    return json.dumps(response.json()[:5])


# Define the tool for the agent
coin_list_tool = {
    "type": "function",
    "function": {
        "name": "coin_list_with_market_data",
        "description": "Fetches the top 5 cryptocurrencies with market data from CoinGecko.",
        "call": coin_list_with_market_data,  # Attach the function to the tool
    },
}

# Create the agent
crypto_agent = Agent(
    name="crypto-agent",
    model=OpenAIChat(id="gpt-4"),  # Specify model ID
    tools=[coin_list_with_market_data],  # Register tools
    tool_choice={
        "type": "function",
        "function": {"name": "coin_list_with_market_data"},
    },  # Let the agent decide on tool usage
    show_tool_calls=True,
    instructions=[
        "You are an expert in cryptocurrency with a deep understanding of cryptocurrency markets.",
    ],
    markdown=True,
)

# Test the agent with a query
response = crypto_agent.run(
    "What is the best coin to invest in at this moment, and which market should I target?"
)
print("Agent response:")
print(response)
