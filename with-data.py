import requests
from phi.agent import Agent
from phi.knowledge.json import JSONKnowledgeBase
from phi.vectordb.pgvector import PgVector

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

knowledge_base = JSONKnowledgeBase(
    path="./data/data.json",
    # Table name: ai.json_documents
    vector_db=PgVector(
        table_name="json_documents",
        db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
    ),
)


def get_token_price(token_id: str, currency: str = "usd") -> str:
    """Use this function to get the price of a token in a specific currency.

    Args:
        token_id (str): The id of the token. This is passed by the Agent.
        currency (str): The currency to fetch the price in. Default is 'usd'.

    Returns:
        str: The price of the token in the specified currency.
    """
    url = "https://api.coingecko.com/api/v3/simple/price"
    headers = {"x-cg-demo-api-key": "CG-avYkqe4B6teKU5KYGfNgCua1"}
    params = {"ids": token_id, "vs_currencies": currency}

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        price = data.get(token_id, {}).get(currency, None)
        if price is not None:
            return f"The price of {token_id} is {price} {currency.upper()}."
        else:
            return f"Unable to fetch the price for {token_id}."
    except Exception as e:
        return f"An error occurred: {e}"


# Register the tools with the Agent

agent = Agent(
    knowledge=knowledge_base,
    search_knowledge=True,
    tools=[get_token_price],
    show_tool_calls=True,
    instructions=[
        "You must search for the coin id on your knowledge database",
        "The name provided by user might be incorreclty typed",
        "So search for the closet thing that the user might mean",
        "Possibly show all the possible values and then pass it to the function and return all the possible answers",
        "After retriving the token_id from the knowledge you will pass it to the `get_token_price` function",
    ],
)
agent.knowledge.load(recreate=False)


# Example usage
# agent.print_response("What is the price of baby-Trump in EUR?", stream=True)
# agent.print_response("What is the price of Trump in EUR?", stream=True)
# agent.print_response("What is the price of Pepe in USD?", stream=True)
agent.print_response("What is the price of Bitcoin in USD?", stream=True)
