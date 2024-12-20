# This is wikepedia.py
import os
import json
import asyncio
from typing import List, Dict, Any
import requests
from dotenv import load_dotenv
from groq import Groq


load_dotenv()

class Tool:
    @staticmethod
    def wikipedia_search(query: str) -> str:
        """Search Wikipedia for a query."""
        try:
            response = requests.get(
                "https://en.wikipedia.org/w/api.php",
                params={
                    "action": "query",
                    "format": "json",
                    "list": "search",
                    "srsearch": query
                }
            )
            data = response.json()
            if data['query']['searchinfo']['totalhits'] > 0:
                return data['query']['search'][0]['snippet']
            return "No results found."
        except Exception as e:
            return f"Error in Wikipedia search: {str(e)}"
