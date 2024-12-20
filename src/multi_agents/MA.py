# This is MA.py
import os
import json
import asyncio
from typing import List, Dict, Any
import requests
from dotenv import load_dotenv
from groq import Groq
from src.agents.BASE_AGENT import Agent
from src.tools.wikepedia import Tool
load_dotenv()


class MultiAgentSystem:
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
        self.agents: List[Agent] = [
            Agent("StrategicAnalyst", "Provide high-level strategic insights", self.client),
            Agent("ResearchSpecialist", "Conduct deep, detailed research", self.client),
            Agent("CreativeThinker", "Generate innovative perspectives", self.client),
            Agent("EthicalConsiderator", "Evaluate ethical implications", self.client),
            Agent("ReportEditor", "Synthesize results into a cohesive report", self.client),
        ]

    async def collaborative_reasoning(self, task: str, iterations: int = 3) -> List[Dict[str, Any]]:
        """
        Collaborative reasoning across multiple agents
        """
        all_results = []
        best_iteration = None
        best_quality = -float('inf')  # To store the best iteration's quality score
        context = Tool.wikipedia_search(task) if hasattr(Tool, 'wikipedia_search') else ""

        for iteration in range(iterations):
            # Concurrent agent reasoning
            try:
                iteration_results = await asyncio.gather(
                    *[agent.reason(task, context) for agent in self.agents],
                    return_exceptions=True
                )
            except Exception as e:
                iteration_results = [{"error": f"Iteration error: {str(e)}"}]

            # Calculate quality metric (e.g., based on content length or keyword match)
            quality_metric = sum(len(result.get('reasoning', '')) for result in iteration_results if isinstance(result, dict))

            # Update best iteration based on quality metric
            if quality_metric > best_quality:
                best_quality = quality_metric
                best_iteration = iteration_results

            # Update context with new insights
            context += " " + " ".join(
                [result.get('reasoning', '') for result in iteration_results if isinstance(result, dict)]
            )
            all_results.extend(iteration_results)

        return best_iteration or all_results

    def generate_final_report(self, task: str, results: List[Dict[str, Any]]) -> str:
        """Generate a cohesive final report"""
        introduction = f"### Introduction\nThis report analyzes the task: '{task}'. Below, we present consolidated insights from multiple AI agents.\n\n"
        analysis = "### Analysis\n"
        for result in results:
            agent_name = result.get("agent", "Unknown Agent")
            reasoning = result.get("reasoning", "").strip()
            if reasoning:
                analysis += f"- **{agent_name}**: {reasoning}\n\n"
        
        conclusion = "### Conclusion\nBased on the insights, the following conclusions and recommendations can be drawn:\n"
        conclusion += "- (Insert key conclusions and actionable recommendations here)\n"

        return f"# Multi-Agent Analysis Report: {task}\n\n{introduction}{analysis}{conclusion}"

    async def process_task(self, task: str, iterations: int = 3) -> str:
        """End-to-end processing of a task"""
        results = await self.collaborative_reasoning(task, iterations)
        return self.generate_final_report(task, results)
