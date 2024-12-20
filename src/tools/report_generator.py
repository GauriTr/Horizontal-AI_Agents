import json
from typing import List, Dict, Any
from datetime import datetime

class ReportGenerator:
    @staticmethod
    def generate_professional_report(task: str, results: List[Dict[str, Any]], research_data: str = "") -> str:
        """Generate a professional news-style report"""
        # Extract key insights from results
        insights = [r.get('reasoning', '') for r in results if isinstance(r, dict)]
        
        # Format current date
        current_date = datetime.now().strftime("%B %d, %Y")
        
        report = f"""# Professional Analysis Report
*Generated on {current_date}*

## Executive Summary
{ReportGenerator._generate_executive_summary(task, insights)}

## Detailed Analysis
{ReportGenerator._generate_detailed_analysis(insights)}

## Expert Perspectives
{ReportGenerator._generate_expert_perspectives(results)}


## Conclusions and Implications
{ReportGenerator._generate_conclusions(insights)}

---
*This report was generated using advanced AI analysis and expert system evaluation.*
"""
        return report

    @staticmethod
    def _generate_executive_summary(task: str, insights: List[str]) -> str:
        # Combine insights and generate a concise summary
        combined_insights = " ".join(insights)
        return f"This comprehensive analysis examines {task}, focusing on key aspects and implications derived from multiple expert perspectives..."

    @staticmethod
    def _generate_detailed_analysis(insights: List[str]) -> str:
        analysis = ""
        for idx, insight in enumerate(insights, 1):
            if insight and len(insight) > 50:
                # Filter out action steps and keep only thoughts and observations
                filtered_insight = ReportGenerator._extract_thoughts_and_observations(insight)
                if filtered_insight:
                    analysis += f"### Key Finding {idx}\n{filtered_insight}\n\n"
        return analysis

    @staticmethod
    def _generate_expert_perspectives(results: List[Dict[str, Any]]) -> str:
        perspectives = ""
        for result in results:
            if isinstance(result, dict) and result.get('reasoning'):
                agent_name = result.get('agent', 'Expert Analyst')
                perspective = result.get('reasoning', '').split('.')[0] + '.'  # First sentence only
                perspectives += f"**{agent_name}**: {perspective}\n\n"
        return perspectives


    @staticmethod
    def _generate_conclusions(insights: List[str]) -> str:
        return "Based on the analyzed data and expert insights, the following conclusions can be drawn:\n\n" + \
               "1. [Key conclusion derived from analysis]\n" + \
               "2. [Implications for stakeholders]\n" + \
               "3. [Future outlook and recommendations]"

    @staticmethod
    def _extract_thoughts_and_observations(text: str) -> str:
        """Extract only thoughts and observations from agent reasoning"""
        lines = text.split('\n')
        filtered_content = []
        for line in lines:
            line = line.strip()
            if line.startswith(('Thought:', 'Observation:')) or not any(x in line.lower() for x in ['action:', 'tool[']):
                filtered_content.append(line)
        return '\n'.join(filtered_content)

    @staticmethod
    def generate_reasoning_log(task: str, all_iterations: List[List[Dict[str, Any]]], iteration_count: int) -> str:
        """Generate detailed reasoning logs including all iterations"""
        log = f"Detailed Reasoning Log for Task: {task}\n"
        log += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        log += "=" * 80 + "\n\n"

        for iter_num, iteration in enumerate(all_iterations, 1):
            log += f"Iteration {iter_num}/{iteration_count}\n"
            log += "-" * 40 + "\n"
            
            for result in iteration:
                if isinstance(result, dict):
                    agent_name = result.get('agent', 'Unknown Agent')
                    reasoning = result.get('reasoning', '')
                    
                    log += f"\nAgent: {agent_name}\n"
                    log += f"Role: {result.get('role', 'N/A')}\n"
                    log += "Full Reasoning Process:\n"
                    log += f"{reasoning}\n"
                    log += "-" * 30 + "\n"
            
            log += "\n" + "=" * 80 + "\n\n"
        
        return log
