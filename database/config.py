from pydantic import BaseModel, Field
from typing import Literal, Optional

class Creat_agents(BaseModel):
    name: str = Field(max_length=30)
    specialty: str = Field(max_length=50)
    agent_renk:Literal['Junior', 'Senior', 'Commander']

class Update_agents(BaseModel):
    name:Optional[str] 
    specialty:Optional[str]
    agent_renk:Optional[str]

class Create_mission(BaseModel):
    title:str
    description:str
    location:str
    difficulty:int 
    importance:int 




