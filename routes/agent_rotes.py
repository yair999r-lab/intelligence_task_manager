from fastapi import APIRouter, HTTPException, status
from database.config import Creat_agents, Update_agents
from database.agent_db import AgentDB

ca = AgentDB()

route = APIRouter(prefix='/agents', tags=['agent'])

@route.post(status_code=status.HTTP_201_CREATED)
def add_agebt(data:Creat_agents):
    agent = ca.create_agent(data=data.model_dump())
    if agent:
        return agent
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

@route.get(status_code=status.HTTP_200_OK)
def show_all_agent():
    return ca.get_all_agents()

@route.get('/{id}', status_code=status.HTTP_200_OK)
def show_agent(id:int):
    agent = ca.get_agent_by_id(id=id)
    if agent:
        return agent
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
@route.put('/{id}', status_code=status.HTTP_200_OK)
def update_agents(id:int, data:Update_agents):
    up_data = data.model_dump(exclude_unset=True)
    update = ca.update_agent(id=id, data=up_data)

    if update:
        return update
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    
@route.put('/{id}/deactivate', status_code=status.HTTP_200_OK)
def agent_deactivate(id:int):
    change = ca.deactivate_agent(id=id)

    if change:
        return change
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

@route.get('/{id}/performance', status_code=status.HTTP_200_OK)
def show_agent_performance(id:int):
    performance = ca.get_agent_performance(id=id)

    if performance:
        return performance
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    




