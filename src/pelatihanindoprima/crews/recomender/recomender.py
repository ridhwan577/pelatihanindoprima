from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent


@CrewBase
class Recommender():
    """Recommender crew"""

    agents: list[BaseAgent]
    tasks: list[Task]



    @agent
    def recommender(self) -> Agent:
        return Agent(
            config=self.agents_config['recommender'],
            verbose=True
    )


    @task
    def recommendation_task(self) -> Task:
        return Task(
        config=self.tasks_config['recommendation_task'],
    )

    @crew
    def crew(self) -> Crew:
        """Creates the Recommender crew"""
      
        return Crew(
            agents=self.agents, 
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
        )
