from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import FileReadTool
from pydantic import BaseModel, Field
from typing import List

@CrewBase
class FileAnalyzer():
    """FileAnalyzer crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    fileReadTool=FileReadTool()

    class Output_txt_analyzer(BaseModel):
        insight:str
        indicator:str

    @agent
    def agent_file_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['agent_file_analyzer'], # type: ignore[index]
            verbose=True,
            tools = [self.fileReadTool]
        )

    class Output_txt_analyzer_schema(BaseModel):
        analyzer : list["Output_txt_analyzer"] = Field(..., min_length=5)

    @task
    def task_agent_analyzer(self) -> Task:
        return Task(
            config=self.tasks_config['task_file_analyzer'], # type: ignore[index]

            output_json = self.Output_txt_analyzer
        )


    @crew
    def crew(self) -> Crew:
        """Creates the FileAnalyzer crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
        )
