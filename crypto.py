from phi.agent import Agent
from phi.model.anthropic import Claude
import requests
import json

def coin_list_with_market_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"

    params = {"vs_currency": "usd"}
    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers, params=params)
    return json.dumps(response.json()[:5])

crypto_agent = Agent(
    # specifying models
    name="crypto-agent",
    model=Claude(id="claude-3-5-sonnet-20240620"),
    # specifying tools
    tools=[coin_list_with_market_data],
    tool_choice={"type": "function", "function": {"name": "coin_list_with_market_data"}},
    show_tool_calls=True,
    # instructions and misc
    instructions=["You are a expert in cryptocurrency who have a deep understanding of cryptocurrency markets"],
    markdown=True,
)

crypto_agent.print_response(
    "What is the best coin to invest at this moment and which market should I target?", stream=True
)
