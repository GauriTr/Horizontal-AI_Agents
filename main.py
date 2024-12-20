import os, json, asyncio, requests
from typing import List, Dict, Any
from dotenv import load_dotenv
from groq import Groq
from src.multi_agents.MA import MultiAgentSystem

load_dotenv()


async def main():

    api_key = os.getenv('GROQ_API_KEY')
    task = "Current Trend in Full stack development"
    agent_system = MultiAgentSystem(api_key)
    # Get both report and detailed log
    final_report, detailed_log = await agent_system.process_task(task)
    with open('README.md', 'w') as f:
        f.write(final_report)
    # Save the detailed reasoning log
    with open('detailed_reasoning_log.txt', 'w') as f:
        f.write(detailed_log)
    print("Multi-Agent Reasoning Report and Detailed Log Generated Successfully!")

if __name__ == "__main__":
    asyncio.run(main())