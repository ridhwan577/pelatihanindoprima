from logging import config

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from src.pelatihanindoprima.tools.tool_helmet_detection import Tool_helmet_detection

@CrewBase
class CrewDeteksiHelmet():
    
    agents: list[BaseAgent]
    tasks: list[Task]
    agents_config: "config/agents.yaml"
    tasks_config: "config/tasks.yaml"

  
    def agent_helmet_detection(self) -> Agent:
        return Agent(
            config=self.agents_config['agent_helmet_detection'],
            verbose=True
        )
    
    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            verbose=True
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['reporting_analyst'],
            verbose=True
        )


    @task
    def task_helmet_detection(self) -> Task:
        return Task(
            config=self.tasks_config['task_helmet_detection'], 
        )
        
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'], 
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the CrewDeteksiHelmet crew"""
        

        return Crew(
            agents=self.agents, 
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
