import os
import json
import asyncio
from typing import List, Dict, Any
import requests
from dotenv import load_dotenv
from groq import Groq
from src.multi_agents.MA import MultiAgentSystem

load_dotenv()


async def main():

    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        raise ValueError("Groq API Key not found. Please set GROQ_API_KEY in .env")


    task = "Current Trend in Full stack development"


    agent_system = MultiAgentSystem(api_key)


    results = await agent_system.collaborative_reasoning(task)


    final_report = agent_system.generate_final_report(task, results)

    with open('README.md', 'w') as f:
        f.write(final_report)

    print("Multi-Agent Reasoning Report Generated Successfully!")

if __name__ == "__main__":
    asyncio.run(main())