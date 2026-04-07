from tools import calculator, weather, summarize

TOOLS = [
    {"name": "calculator", "keywords": ["calculate","calc","compute","+","-","*","/","^"], "fn": calculator},
    {"name": "weather", "keywords": ["weather","temperature","forecast","humid"], "fn": weather},
    {"name": "summarize", "keywords": ["summarize","summary","tldr","shorten"], "fn": summarize},
]

def select_tool(query: str):
    q = query.lower()
    for tool in TOOLS:
        if any(kw in q for kw in tool["keywords"]):
            return tool
    return None

def run_agent():
    print("=" * 55)
    print(" Tool-Using AI Agent (Task 2)")
    print(" Tools: calculator | weather  | summarize ")
    print(" Type 'exit' to quit")
    print("=" * 55)
    while True:
        query = input("\nYou: ").strip()
        if not query: 
            continue
        if query.lower() in ("exit","quit"): 
            print("Bye!")
            break
        tool = select_tool(query)
        if tool:
            print(f"[Agent] Using tool: {tool['name']}")
            print(f"Agent: {tool['fn'](query)}")
        else:
            print("Agent: No matching tool found. Try: calculate, weather, summarize.")

if __name__ == "__main__":
    run_agent()
