from phi.agent import Agent
from phi.knowledge.json import JSONKnowledgeBase
from phi.vectordb.pgvector import PgVector

from dotenv import load_dotenv

# from toolkit import CoinGeckoToolkit
from coingeckoTool import CoinGeckoTools

# Load environment variables from .env file
load_dotenv()

knowledge_base = JSONKnowledgeBase(
    path="./data/data.json",
    # Table name: ai.json_documents
    vector_db=PgVector(
        table_name="json_documents",
        db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
    ),
    num_documents=10,
)


# Register the tools with the Agent

agent = Agent(
    knowledge=knowledge_base,
    search_knowledge=True,
    # tools=[CoinGeckoToolkit()],
    tools=[CoinGeckoTools()],
    show_tool_calls=True,
    debug_mode=True,
    instructions=[
        "First you have to find the correct `id` of the coin user is trying to search",
        "look for unnecessay words that are part of the question and not part of the coin name, discard those words and find the accurate word for the coin",
        "Sanitize the user input before searching for the id in the knowledge, remove unnecessay words, spaces with hipiens",
        "Look throughly for the exact coin `id` in the knowledge exactly matching the user input",
        "The user input should match the the id, symbol and name in the knowledge, query for all the fields and find out which one matches the most",
        "The id should match exactly with the user input",
        "If exact not found, find the related results",
        "Dont ask for the users confirmation, search using those related results you have found",
        "also detect the currency in the user input, convert the currency in lowercase and pass it to the CoinGeckoToolkit functions",
        "Search for the token price by passing the id as a argument in the CoinGeckoToolkit functions",
        "Execute the actions for those results using the CoinGeckoToolkit functions",
    ],
)
agent.knowledge.load(recreate=False)


# Example usage
# agent.print_response("What is the price of baby-Trump in EUR?", stream=True)
# agent.print_response("What is the price of Trump in EUR?", stream=True)
# agent.print_response("What is the price of Pepe in INR?", stream=True)
# agent.print_response("What is the price of MAGA Trump in USD?", stream=True)
# agent.print_response("What is the price of Bitcoin in USD?", stream=True)
# agent.print_response("Tell me the market cap for bitcoin", stream=True)
# agent.print_response("Tell me about bitcoin", stream=True)
# agent.print_response("Tell me about pepe coin", stream=True)
agent.print_response(
    "Tell me about latest trump coin that is created by Donuld trump", stream=True
)
