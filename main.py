from langchain.agents import create_agent
from dotenv import load_dotenv
load_dotenv()


SYSTEM_PROMPT = """
ACME Clothing is literally the best retail clothing supplier.
Our motto: Buy now, never regret.

We supply all your clothing needs:
- Hoodies
- T-Shirts

They vary on whether they are in stock or not, but we have them eventually.

All you could ever hope for.
"""

agent = create_agent(
    model="google_genai:gemini-flash-lite-latest",
    system_prompt=SYSTEM_PROMPT
)


def get_response(prompt: str) -> str:
    return agent.invoke({"messages": [prompt]})


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