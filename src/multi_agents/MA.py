# This is MA.py
import os, json, asyncio, requests
from typing import List, Dict, Any
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

    async def collaborative_reasoning(self, task: str, iterations: int = 3) -> tuple[List[Dict[str, Any]], List[List[Dict[str, Any]]]]:
        """
        Collaborative reasoning across multiple agents
        Returns both best iteration and all iterations history
        """
        all_iterations = []  # Store all iterations
        best_iteration = None
        best_quality = -float('inf')
        context = Tool.wikipedia_search(task) if hasattr(Tool, 'wikipedia_search') else ""

        for iteration in range(iterations):
            try:
                iteration_results = await asyncio.gather(
                    *[agent.reason(task, context) for agent in self.agents],
                    return_exceptions=True
                )
            except Exception as e:
                iteration_results = [{"error": f"Iteration error: {str(e)}"}]

            all_iterations.append(iteration_results)  # Store each iteration's results
            
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

        return best_iteration or all_iterations[-1], all_iterations

    def generate_final_report(self, task: str, results: List[Dict[str, Any]]) -> str:
        """Generate a professional report using ReportGenerator"""
        from src.tools.report_generator import ReportGenerator
        context = Tool.wikipedia_search(task) if hasattr(Tool, 'wikipedia_search') else ""
        return ReportGenerator.generate_professional_report(task, results, context)

    async def process_task(self, task: str, iterations: int = 3) -> tuple[str, str]:
        """End-to-end processing of a task, returns both report and detailed log"""
        results, all_iterations = await self.collaborative_reasoning(task, iterations)
        
        # Generate the main report
        final_report = self.generate_final_report(task, results)
        
        # Generate the detailed reasoning log
        from src.tools.report_generator import ReportGenerator
        detailed_log = ReportGenerator.generate_reasoning_log(task, all_iterations, iterations)
        
        return final_report, detailed_log
