from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task, before_kickoff
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from .tools import search_tool, file_writer_tool, file_read_tool
import os
from datetime import datetime

@CrewBase
class Podcaster():
    """Podcaster crew"""
    agents: List[BaseAgent]
    tasks: List[Task]

    groq_llm = LLM(
        model="groq/llama-3.1-8b-instant",
        api_key=os.environ.get("GROQ_API_KEY"),
        temperature=0.5,
        max_tokens=300
    )

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            verbose=True,
            llm=self.groq_llm
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['reporting_analyst'],
            verbose=True,
            llm=self.groq_llm
        )

    @agent
    def scriptwriter(self) -> Agent:
        return Agent(
            config=self.agents_config['scriptwriter'],
            verbose=True,
            llm=self.groq_llm,
            tools=[]   
        )

    @before_kickoff
    def _ensure_outputs_dir(self, inputs=None):
        os.makedirs(os.path.join(os.getcwd(), 'outputs'), exist_ok=True)
        return inputs

    @task
    def research_task(self) -> Task:
        return Task(config=self.tasks_config['research_task'])

    @task
    def reporting_task(self) -> Task:
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        return Task(
            config=self.tasks_config['reporting_task'],
            output_file=os.path.join('outputs', f'report-{timestamp}.md')
        )

    @task
    def scripting_task(self) -> Task:
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        return Task(
            config=self.tasks_config['scripting_task'],
            output_file=os.path.join('outputs', f'script-{timestamp}.md')
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )