from urllib import response
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv
load_dotenv()


SYSTEM_PROMPT = """
You are my cooking AI assistant, and will help me get answers to questions I have about different ways of cooking, and help me find recipes I can make with the ingrediants I have.

Users can end the conversation by typing "exit".
"""


@tool ("get_it")
def get_it(item: str, color: str) -> str:
    """
    finds the stock of the item, and says whether it is in stock or not.
    """
    fake_stock = {
    ("hoodie", "blue"): 4,
    ("hoodie", "black"): 12,
    ("t-shirt", "blue"): 30,
    }

    if (item.lower(), color.lower()) in fake_stock:
        return "We're in stock!"
    else:
        return "We're out of stock..."


agent = create_agent(
    model="google_genai:gemini-flash-lite-latest",
    system_prompt=SYSTEM_PROMPT,
    checkpointer=InMemorySaver(),
)


def get_response(prompt: str) -> str:
    response = agent.invoke(
        {"messages": [prompt]},
        {"configurable": {"thread_id": "1"}})
    return response["messages"][-1].text


def main():
    while True:
        try:
            prompt = input("Input: ")
            if prompt == "exit": break
            response = get_response(prompt)
        except EOFError:
            break
        print(response)

if __name__ == "__main__":
    main()