import os, re, json, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "day2"))

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_numbers(query: str) -> list:
    nums = re.findall(r"[-+]?\d*\.?\d+", query)
    return [float(n) for n in nums]

def compute_average(numbers: list) -> float:
    if not numbers:
        raise ValueError("No numbers provided.")
    return sum(numbers) / len(numbers)

def compute_sum(numbers: list) -> float:
    return sum(numbers)

def llm_summarize(context: str) -> str:
    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "Summarize the following mathematical result in one clear sentence for a non-technical user."},
            {"role": "user", "content": context}
        ],
        max_tokens=100
    )
    return resp.choices[0].message.content.strip()

PLAN_PROMPT = """You are a task planner. Given a user request, generate an ordered JSON array of steps.
Each step is: {"step": , "action": "", "description": ""}
Available actions: extract_numbers, compute_average, compute_sum, llm_summarize.
Respond ONLY with the JSON array, no extra text."""

def plan_steps(query: str) -> list:
    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": PLAN_PROMPT},
            {"role": "user", "content": query}
        ],
        max_tokens=300
    )
    raw = resp.choices[0].message.content.strip()
    raw = re.sub(r"```json|```", "", raw).strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return [
            {"step":1,"action":"extract_numbers","description":"Extract numbers"},
            {"step":2,"action":"compute_average","description":"Compute average"},
            {"step":3,"action":"llm_summarize", "description":"Summarize result"}
        ]

def execute_plan(query: str, steps: list):
    print("\n--- Execution Plan ---")
    for s in steps:
        print(f" Step {s['step']}: [{s['action']}] {s['description']}")
    
    print()
    context = {"query": query, "numbers": [], "result": None, "summary": ""}
    
    for s in steps:
        action = s["action"]
        print(f"[Step {s['step']}] Executing: {action}")
        
        if action == "extract_numbers":
            context["numbers"] = extract_numbers(query)
            print(f" -> Extracted numbers: {context['numbers']}")
        
        elif action == "compute_average":
            context["result"] = compute_average(context["numbers"])
            print(f" -> Average: {context['result']}")
        
        elif action == "compute_sum":
            context["result"] = compute_sum(context["numbers"])
            print(f" -> Sum: {context['result']}")
        
        elif action == "llm_summarize":
            summary_input = (f"Numbers: {context['numbers']}. "
                           f"Result: {context['result']}")
            context["summary"] = llm_summarize(summary_input)
            print(f" -> Summary: {context['summary']}")
            
    print("\n=== Final Output ===")
    print(f"Numbers : {context['numbers']}")
    print(f"Result  : {context['result']}")
    print(f"Summary : {context['summary']}")

def run_agent():
    print("=" * 60)
    print(" Multi-Step Planning Agent (Task 4)")
    print(" Example: Find the average of 5, 10, 15 and summarize")
    print(" Type 'exit' to quit")
    print("=" * 60)
    
    while True:
        query = input("\nYou: ").strip()
        if not query: 
            continue
        if query.lower() in ("exit","quit"): 
            print("Bye!")
            break
        
        print("\n[Agent] Planning steps via LLM...")
        steps = plan_steps(query)
        execute_plan(query, steps)

if __name__ == "__main__":
    run_agent()
