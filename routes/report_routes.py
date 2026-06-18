from fastapi import APIRouter, status, HTTPException

from database.agent_db import AgentDB
from database.mission_db import MissionDB

route = APIRouter(prefix='/reports', tags=["summry"])

@route.get('/get_top_agent', status_code=status.HTTP_200_OK)
def all_data():
    data = {"active_agents_count": 0,
    "total_missions": 0,
    "open_missions": 0,
    "completed_missions": 0,
    "failed_missions": 0,
    "critical_missions": 0
}
    active = AgentDB().count_active_agents()

    data['active_agents_count'] = len(active)

    total_mission = MissionDB().get_all_mission()
    data['total_missions'] = len(total_mission)

    open_missions = MissionDB().count_open_missions()
    data['open_missions'] = open_missions

    complete = MissionDB().count_by_status("COMPLETED")
    data['completed_missions'] = complete

    failed = MissionDB().count_by_status("FAILED")
    data['failed_missions'] = failed

    criti = MissionDB().count_critical_missions()
    data['critical_missions'] = criti

    return data

@route.get('/missions-by-status', status_code=status.HTTP_200_OK)
def count_status():

    stt = {"open": 0,
"in_progress": 0,
"completed": 0,
"failed": 0,
"canceled": 0
}
    
    stt['open'] = MissionDB().count_open_missions()
    stt['in_progress'] = MissionDB().count_by_status('PROGRESS_IN')
    stt['completed'] = MissionDB().count_by_status('COMPLETED')
    stt['failed'] = MissionDB().count_by_status('FAILED')
    stt['canceled'] = MissionDB().count_by_status('CANCELLED')

    return stt


@route.get('/top-agent')
def get_top():
    return MissionDB().get_top_agent()

