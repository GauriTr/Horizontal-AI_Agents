# This is BASE_AGENT.py
import os, yaml, json, asyncio, requests
from typing import List, Dict, Any
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
You are {self.name}, a professional analyst with expertise in: {self.role}.
Provide clear, journalistic-style analysis following these guidelines:

1. Use formal, professional language
2. Support claims with reasoning
3. Maintain objectivity
4. Focus on key insights and implications
5. Consider broader context and impact

Topic for analysis: {task}

Additional Context: {context}

Format your response as a structured analysis with clear points and supporting details.
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