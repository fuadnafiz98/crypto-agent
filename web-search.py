from phi.agent import Agent
from phi.model.anthropic import Claude
from phi.tools.duckduckgo import DuckDuckGo

web_agent = Agent(
    # specifying models
    name="test-agent",
    model=Claude(id="claude-3-5-sonnet-20240620"),
    # specifying tools
    tools=[DuckDuckGo()],
    show_tool_calls=True,
    # instructions and misc
    instructions=["You are a excellient parser that parses information from websites"],
    markdown=True,
)

web_agent.print_response(
    "What is the best book for learning distributed systems", stream=True
)
