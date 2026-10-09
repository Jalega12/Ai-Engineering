from urllib import response
from click import prompt
from langchain.agents import create_agent
from langchain.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langchain.mcp import MCPAdapter
from dotenv import load_dotenv
import asyncio
import logging
logging.getLogger("google_genai").setLevel(logging.ERROR)
logging.getLogger("langchain_google_genai._function_utils").setLevel(logging.ERROR)
logging.disable(logging.WARNING)

import warnings
from langchain_core._api import LangChainBetaWarning
warnings.filterwarnings("ignore", category=LangChainBetaWarning)


load_dotenv()

memories = []

SYSTEM_PROMPT = """
You are my cooking AI assistant. Help me answer cooking questions, make meal plans,
and find recipes based on my preferences.

Follow these steps for each interaction:

1. User Identification:
   - You should assume that you are interacting with default_user
   - If you have not identified default_user, proactively try to do so.

2. Memory Retrieval:
   - Always begin your chat by saying only "Remembering..." and retrieve all relevant information from your knowledge graph
   - Always refer to your knowledge graph as your "memory"

3. Memory
   - While conversing with the user, be attentive to any new information that falls into these categories:
     a) Basic Identity (age, gender, location, job title, education level, etc.)
     b) Cooking Preferences (favorite foods, dietary restrictions, allergies, etc.)
     c) Relationships (personal and professional relationships up to 3 degrees of separation)

4. Memory Update:
   - If any new information was gathered during the interaction, update your memory as follows:
     a) Create entities for recurring organizations, people, and significant events
     b) Connect them to the current entities using relations
     c) Store facts about them as observations
"""




config = {
    "mcpServers": {
        "memory": {
            "command": "npx",
            "args": [
                "-y",
                "@modelcontextprotocol/server-memory"
            ]
        }
    }
}


async def main():
    async with MCPAdapter(config) as adapter:
        mcp_tools = await adapter.list_tools()

        # Include the custom Python tool alongside MCP tools.
        tools = mcp_tools

        agent = create_agent(
            model="google_genai:gemini-flash-lite-latest",
            tools=tools,
            system_prompt=SYSTEM_PROMPT,
            checkpointer=InMemorySaver(),
        )

        async def get_response(user_prompt: str) -> str:
            result = await agent.ainvoke(
                {
                    "messages": [
                        {"role": "user", "content": user_prompt}
                    ]
                },
                {"configurable": {"thread_id": "1"}}
            )

            return result["messages"][-1].content

        while True:
            try:
                user_prompt = input("Input: ").strip()

                if user_prompt.lower() == "exit":
                    break

                answer = await get_response(user_prompt)
                print(answer)

            except EOFError:
                break


if __name__ == "__main__":
    asyncio.run(main())