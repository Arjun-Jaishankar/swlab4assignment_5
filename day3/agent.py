import os, re, json, datetime, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "day2"))

from dotenv import load_dotenv
from groq import Groq
from tools import calculator, weather, summarize

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
LOG_FILE = os.path.join(os.path.dirname(__file__), "logs.txt")

TOOLS = {
    "calculator": calculator,
    "weather": weather,
    "summarize": summarize,
}

SYSTEM_PROMPT = """You are a tool-routing AI agent.
Given a user query, respond ONLY with a valid JSON object in this exact format:
{"tool": "", "reason": ""}
Available tools: calculator, weather, summarize.
If none fits, use {"tool": "none", "reason": "..."}
Respond with ONLY the JSON, no extra text."""

def log(entry: dict):
    entry["timestamp"] = datetime.datetime.now().isoformat()
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

def llm_select_tool(query: str) -> str:
    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ],
        max_tokens=80
    )
    raw = resp.choices[0].message.content.strip()
    raw = re.sub(r"```json|```", "", raw).strip()
    try:
        data = json.loads(raw)
        return data.get("tool", "none")
    except json.JSONDecodeError:
        return "none"

def run_agent():
    print("=" * 55)
    print(" LLM-Based Agent (Task 3) — Groq llama-3.1-8b-instant")
    print(" Logs saved to day3/logs.txt")
    print(" Type 'exit' to quit")
    print("=" * 55)
    while True:
        query = input("\nYou: ").strip()
        if not query: 
            continue
        if query.lower() in ("exit","quit"): 
            print("Bye!")
            break
        tool_name = llm_select_tool(query)
        print(f"[LLM selected tool]: {tool_name}")
        if tool_name in TOOLS:
            output = TOOLS[tool_name](query)
        else:
            output = "I could not determine the right tool for your request."
        print(f"Agent: {output}")
        log({"input": query, "tool": tool_name, "output": output})

if __name__ == "__main__":
    run_agent()
