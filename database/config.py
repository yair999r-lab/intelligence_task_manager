from pydantic import BaseModel, Field
from typing import Literal, Optional

class Creat_agents(BaseModel):
    name: str = Field(max_length=30)
    specialty: str = Field(max_length=50)
    agent_renk:Literal['Junior', 'Senior', 'Commander']

class Update_agents(BaseModel):
    name:Optional[str] = Field(default=None, max_length=30)
    specialty:Optional[str] = Field(default=None, max_length=50)
    agent_renk:Optional[str] = Literal['Junior', 'Senior', 'Commander']

class Create_mission(BaseModel):
    title:str
    description:str
    location:str
    difficulty:int = Field(ge=1, le=10)
    importance:int = Field(ge=1, le=10)


def risk_level_calculation(data: dict):
        risk = data['difficulty'] * 2 + data['importance']
        if risk < 10:
            return 'LOW'
        elif risk < 17:
            return "MEDIUM"
        elif risk < 25:
            return "HIGH"
        else:
            return "CRITICAL"




