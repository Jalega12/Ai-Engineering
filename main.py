from langchain.agents import create_agent


SYSTEM_PROMPT = """
ACME Clothing is literally the best retail clothing supplier.
Our motto: Buy now, never regret.

We supply all your clothing needs:
- Hoodies
- T-Shirts

They vary on whether they are in stock or not, but we have them eventually.

All you could ever hope for.
"""

def get_it(item: str, color: str) -> str:
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
    tools=["get_it"]
    system_prompt=SYSTEM_PROMPT
)


def get_it(item: str, color: str) -> str:
    fake_stock = {
        ("hoodie", "blue"): 4,
        ("hoodie", "black"): 12,
        ("t-shirt", "blue"): 30,
    }

    if (item.lower(), color.lower()) in fake_stock:
        return "We're in stock!"
    else:
        return "We're out of stock..."
    
print("hi")