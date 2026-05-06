from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
import mysql.connector

class Tool_save_to_db_input(BaseModel):
    person: int = Field(..., description="Number of people detected in the image.")
    helmet: int = Field(..., description="Number of helmets detected in the image.")
    head: int = Field(..., description="Number of heads detected in the image.")
    

class Tool_save_to_db(BaseTool):
    name: str = "Save to Database Tool"
    description: str = "Tool for saving data to the database"
    args_schema: Type[BaseModel] = Tool_save_to_db_input
    
    def _run(self, head: int, person: int, helmet: int) -> str:
        connection = None
        cursor = None
        try:
            connec = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="",
                database="indoprima",
            )
            cursor = connec.cursor()
            if (head > 0):
                detil = f"{head} head(s) detected,{person} person(s) detected, {helmet} helmet(s) detected"
                query = "INSERT INTO helmet_report(report_result, report_detected) VALUES (%s, %s)"
                cursor.execute(query, (detil, head))
                connec.commit()
                
                return "Data saved to database successfully."
            else:
                return "Everybody is safety"
        except Exception as e:
            print(f"Error occurred while saving to database: {e}")
        finally:
            if cursor:
                cursor.close()
            if connec and connec.is_connected():
                connec.close()