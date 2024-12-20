# This is BASE_AGENT.py
import os
import json
import asyncio
from typing import List, Dict, Any
import requests
from dotenv import load_dotenv
from groq import Groq


load_dotenv()

class Agent:
    def __init__(self, name: str, role: str, client: Groq):
        self.name = name
        self.role = role
        self.client = client
        self.conversation_history: List[Dict[str, str]] = []

    async def reason(self, task: str, context: str = "") -> Dict[str, Any]:
        """
        Async method for agent reasoning using Groq LLM
        """
        system_prompt = f"""
You are {self.name}, an AI agent with the role: {self.role}.
Using the ReAct (Reasoning and Acting) framework to complete given tasks efficiently. Your thought process should follow this loop: Thought, Action, Observation.
Your task is to systematically analyze and reason about: {task}

Reasoning Guidelines:
1. Break down the problem logically
2. Consider multiple perspectives
3. Provide clear, structured insights
4. Be concise but comprehensive

Context: {context}

For each step:
1. Thought: Explain your reasoning and next steps.
2. Action: Use one of the available tools in the format Tool[input].
3. Observation: Wait for the result of the action.

Repeat this process until you have enough information to provide a final answer.
"""

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": task}
                ],
                model="llama3-70b-8192"
            )
            
            response = chat_completion.choices[0].message.content
            self.conversation_history.append({"task": task, "response": response})
            
            return {
                "agent": self.name,
                "role": self.role,
                "reasoning": response
            }
        
        except Exception as e:
            error_message = str(e)
            self.conversation_history.append({"task": task, "error": error_message})
            return {
                "agent": self.name,
                "error": error_message
            }