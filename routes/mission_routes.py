from fastapi import APIRouter, status, HTTPException

from database.agent_db import AgentDB
from database.mission_db import MissionDB
from database.config import Create_mission
from database.agent_db import AgentDB

cm = MissionDB()

route = APIRouter(prefix="/missions", tags=['missions'])

@route.post('/', status_code=status.HTTP_201_CREATED)
def add_mission(data: Create_mission):
    s_data = data.model_dump()
    try:
        mission = cm.create_mission(data=s_data)
    except:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="missing data")
    
    if mission:
        return mission
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="importance and difficulty must by bytwin 1-10")

@route.get('/', status_code=status.HTTP_200_OK)
def show_all_mission():
    return cm.get_all_mission()

@route.get('/{id}', status_code=status.HTTP_200_OK)
def show_mission(id:int):
    mission = cm.get_mission_by_id(id=id)
    if mission:
        return mission
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="id not exists")
    
@route.put('/{id}/assign/{agent_id}')
def assing_mission(id:int, agent_id:int):
    agent = AgentDB().get_agent_by_id(id=agent_id)
    if not agent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="agent not exists")
    mission = cm.get_mission_by_id(id=id)
    if not mission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="mission not exists")
    if mission['status'] != "NEW":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="mission Already active")
    if agent['is_active'] == False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="agent not active")
    open_mission = cm.get_open_missions_by_agent(id=agent_id)
    if open_mission > 2:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="the agent are already 3 open tasks.")
    if agent['agent_renk'] != "Commander" and mission['risk_level'] == "CRITICAL":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The agent's rank does not match the mission's risk level.")
    assing = cm.assign_mission(id_a=agent_id, id_m=id)

    if assing:
        return assing
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="mission not assign")
    
@route.put('/{id}/start')
def start_mission(id:int):
    mission = cm.get_mission_by_id(id)
    if not mission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="mission not exists")
    if mission['status'] != "ASSIGNED":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="mission status Already active/finished")
    new_stt = cm.update_mission_status(id_m=id, status="PROGRESS_IN")
    if new_stt:
        return new_stt
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="status not change")
    
@route.put('/{id}/complet')
def complet_mission(id:int):
    mission = cm.get_mission_by_id(id)
    if not mission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="mission not exists")
    if mission['status'] != "PROGRESS_IN":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="mission status Already active/finished")
    new_stt = cm.update_mission_status(id_m=id, status="COMPLETED")
    if new_stt:
        incres = AgentDB().incrment_completed(id=mission['assigned_agent_it'])
        if not incres:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        return incres
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="status not change")
    
@route.put('/{id}/fail')
def failed_mission(id:int):
    mission = cm.get_mission_by_id(id)
    if not mission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="mission not exists")
    if mission['status'] != "PROGRESS_IN":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="mission status Already active/finished")
    new_stt = cm.update_mission_status(id_m=id, status="FAILED")
    if new_stt:
        decres = AgentDB().incrment_failed(id=mission['assigned_agent_it'])
        if not decres:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        return decres
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="status not change")
    
@route.put('/{id}/cancel')
def cancel_mission(id:int):
    mission = cm.get_mission_by_id(id)
    if not mission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="mission not exists")
    if mission['status'] not in ["NEW", "ASSIGEND"] :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="mission status Already active/finished")
    new_stt = cm.update_mission_status(id_m=id, status="CANCELLED")
    if new_stt:
        return new_stt
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="status not change")
    


