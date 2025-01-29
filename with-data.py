from phi.agent import Agent
from phi.knowledge.json import JSONKnowledgeBase
from phi.vectordb.pgvector import PgVector

from dotenv import load_dotenv
from toolkit import CoinGeckoToolkit

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


# Register the tools with the Agent

agent = Agent(
    knowledge=knowledge_base,
    search_knowledge=True,
    tools=[CoinGeckoToolkit()],
    show_tool_calls=True,
    debug_mode=True,
    instructions=[
        "Dont halucinate no the token price",
        "First you have to find the correct `id` of the coin user is trying to search",
        "Sanitize the user input before searching for the id in the knowledge, remove unnecessay words, spaces with hipiens",
        "Look throughly for the exact coin `id` in the knowledge exactly matching the user input",
        "If exact not found, find the related results",
        "Dont ask for the users confirmation, search using those related results you have found",
        "Search for the token price by passing the id as a argument in the CoinGeckoToolkit functions",
        "Execute the actions for those results using the CoinGeckoToolkit functions",
    ],
)
agent.knowledge.load(recreate=False)


# Example usage
# agent.print_response("What is the price of baby-Trump in EUR?", stream=True)
# agent.print_response("What is the price of Trump in EUR?", stream=True)
# agent.print_response("What is the price of the coin Pepe in USD?", stream=True)
# agent.print_response("What is the price of MAGA Trump in USD?", stream=True)
agent.print_response("What is the price of Bitcoin in USD?", stream=True)
