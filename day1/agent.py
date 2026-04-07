import re
import datetime

def handle_greeting(query: str) -> str:
    return "Hello! How can I help you today?"

def handle_date(query: str) -> str:
    today = datetime.date.today().strftime("%A, %B %d, %Y")
    return f"Today's date is: {today}"

def handle_calculate(query: str) -> str:
    match = re.search(r'([\d.]+)\s*([+\-*/])\s*([\d.]+)', query)
    if not match:
        return "Sorry, I could not parse a math expression."
    a, op, b = float(match.group(1)), match.group(2), float(match.group(3))
    ops = {"+": a+b, "-": a-b, "*": a*b, "/": (a/b if b!=0 else None)}
    result = ops[op]
    if result is None:
        return "Error: Division by zero."
    return f"Result: {a} {op} {b} = {result}"

def handle_unknown(query: str) -> str:
    return "I did not understand your request. Try: hello, date, calculate 5 + 3"

INTENT_RULES = [
    (["hello", "hi", "hey", "greet"], handle_greeting),
    (["date", "today", "day", "time"], handle_date),
    (["calculate", "calc", "compute", "+", "-", "*", "/", "plus", "minus"], handle_calculate),
]

def detect_intent(query: str):
    q_lower = query.lower()
    for keywords, handler in INTENT_RULES:
        if any(kw in q_lower for kw in keywords):
            return handler
    return handle_unknown

def run_agent():
    print("=" * 50)
    print(" Rule-Based AI Agent (Task 1)")
    print(" Type 'exit' to quit")
    print("=" * 50)
    while True:
        query = input("\nYou: ").strip()
        if not query:
            continue
        if query.lower() in ("exit", "quit", "bye"):
            print("Agent: Goodbye!")
            break
        handler = detect_intent(query)
        response = handler(query)
        print(f"Agent: {response}")

if __name__ == "__main__":
    run_agent()
