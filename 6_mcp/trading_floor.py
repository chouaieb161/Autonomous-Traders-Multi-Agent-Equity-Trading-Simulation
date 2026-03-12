from traders import Trader
from typing import List
import asyncio
from tracers import LogTracer
from agents import add_trace_processor
from market import is_market_open
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv(override=True)

RUN_EVERY_N_MINUTES = int(os.getenv("RUN_EVERY_N_MINUTES", "60"))
RUN_EVEN_WHEN_MARKET_IS_CLOSED = (
    os.getenv("RUN_EVEN_WHEN_MARKET_IS_CLOSED", "true").strip().lower() == "true"
)
USE_MANY_MODELS = os.getenv("USE_MANY_MODELS", "true").strip().lower() == "true"

names = ["Warren", "George", "Ray", "Cathie"]
lastnames = ["Patience", "Bold", "Systematic", "Crypto"]

# Model IDs: Azure, DeepSeek (DEEPSEEK_API_KEY), Gemini (GOOGLE_API_KEY), Grok (GROK_API_KEY)
if USE_MANY_MODELS:
    model_names = [
        "gpt-4.1-mini",           # Azure OpenAI
        "deepseek-chat",          # DeepSeek API
        "gemini-1.5-flash",      # Google Gemini (GOOGLE_API_KEY)
        "grok-2-mini",            # x.ai Grok
    ]
    short_model_names = ["Azure GPT 4.1 Mini", "DeepSeek", "Gemini 1.5 Flash", "Grok 2 Mini"]
else:
    model_names = ["gpt-4.1-mini"] * 4
    short_model_names = ["GPT 4.1 Mini"] * 4


def create_traders() -> List[Trader]:
    traders = []
    for name, lastname, model_name in zip(names, lastnames, model_names):
        traders.append(Trader(name, lastname, model_name))
    return traders


async def run_every_n_minutes():
    add_trace_processor(LogTracer())
    traders = create_traders()
    print(f"✅ Created traders: {', '.join([t.name for t in traders])}")
    print(f"📊 Models: {', '.join([t.model_name for t in traders])}")
    run_count = 0
    while True:
        run_count += 1
        print("\n" + "=" * 60)
        print(f"🔄 Run #{run_count} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)

        if RUN_EVEN_WHEN_MARKET_IS_CLOSED or is_market_open():
            print("📈 Running traders...")
            await asyncio.gather(*[trader.run() for trader in traders])
        else:
            print("Market is closed, skipping run")
        print(f"⏳ Sleeping for {RUN_EVERY_N_MINUTES} minute(s)...")
        await asyncio.sleep(RUN_EVERY_N_MINUTES * 60)


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Starting trading floor scheduler")
    print("=" * 60)
    print(f"⏰ Run every {RUN_EVERY_N_MINUTES} minute(s)")
    print(f"🕒 Run even when market closed: {RUN_EVEN_WHEN_MARKET_IS_CLOSED}")
    print(f"🤖 Use many models: {USE_MANY_MODELS}")
    print("=" * 60)
    asyncio.run(run_every_n_minutes())
