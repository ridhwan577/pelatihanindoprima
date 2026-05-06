from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool, tool
from ultralytics import YOLO
import json


class Tool_helmet_detectionInput(BaseModel):
    file: str = Field(..., description="Path to the image file for helmet detection.")


class Tool_helmet_detection(BaseTool):
    name: str = "Helmet Detection Tool"
    description: str = "Detection tool for indentifying not using helmet"
    args_schema: Type[BaseModel] = Tool_helmet_detectionInput


    modelVision: YOLO = YOLO("src/pelatihanindoprima/tools/best.pt")
    def _run(self, image: str) -> str:
        results = self.modelVision(image)
        detected_objects = results[0].boxes.cls.tolist()
        class_names = results[0].names
        object_counts = {}
        person = 0
        helmet = 0
        head = 0
        for hasil in detected_objects:
            class_name = class_names[int(hasil)]
            if (class_name == "head"):
                head = head + 1
            elif (class_name == "helmet"):
                helmet = helmet + 1
            else: 
                person = person + 1
        result_dic = {
            "results": f"Detected {person} person(s), {helmet} helmet(s), and {head} head(s) in the image.",
            "head": head,
            "helmet": helmet,
            "person": person
        }
        return str(result_dic)