import re, os, requests
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

def calculator(query: str) -> str:
    match = re.search(r'([\d.]+)\s*([+\-*/^])\s*([\d.]+)', query)
    if not match:
        return "Could not find a valid expression in your query."
    a, op, b = float(match.group(1)), match.group(2), float(match.group(3))
    ops = {"+": a+b, "-": a-b, "*": a*b, "/": (a/b if b else None), "^": a**b}
    result = ops.get(op)
    return f"{a} {op} {b} = {result}" if result is not None else "Division by zero!"

WEATHER_KEY = os.getenv("OPENWEATHER_API_KEY")

def weather(query: str) -> str:
    words = query.lower().replace("weather", "").replace("in", "").split()
    city = " ".join(w.capitalize() for w in words).strip() or "London"
    url = (f"https://api.openweathermap.org/data/2.5/weather"
           f"?q={city}&appid={WEATHER_KEY}&units=metric")
    try:
        resp = requests.get(url, timeout=8)
        if resp.status_code != 200:
            return f"Could not fetch weather for {city}. Check city name or API key."
        data = resp.json()
        desc = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]
        feels = data["main"]["feels_like"]
        humid = data["main"]["humidity"]
        return (f"Weather in {city}: {desc}. "
                f"Temp: {temp}C (feels like {feels}C), Humidity: {humid}%")
    except Exception as e:
        return f"Weather API error: {e}"

_groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def summarize(query: str) -> str:
    idx = query.lower().find("summarize")
    text = query[idx + len("summarize"):].strip(": ").strip()
    if not text:
        return "Please provide text to summarize after the word 'summarize'."
    chat = _groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "Summarize the following text concisely in 1-2 sentences."},
            {"role": "user", "content": text}
        ],
        max_tokens=150
    )
    return "Summary: " + chat.choices[0].message.content.strip()
