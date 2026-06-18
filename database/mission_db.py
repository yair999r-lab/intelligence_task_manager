from db_connection import db
from config import Create_mission
from agent_db import AgentDB

class missionDB:
    def __init__(self):
        self.connction = db.get_connection()

    def create_mission(self, data:Create_mission):
        risk = self.risk_level_calculation(data)
        if not risk:
            return "importance and difficulty must by bytwin 1-10"
        data['risk_level'] = risk
        set_a = [key for key in data.keys()]
        set_b = " ,".join(set_a)

        val = tuple(data.values())

        cursor = self.connction.cursor()

        sql = f"INSERT INTO missions({set_b}) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, val)

        self.connction.commit()
   
        if cursor.rowcount > 0:
            id = cursor.lastrowid
            cursor.execute(f"SELECT * FROM missions WHERE id={id}")
            agent = cursor.fetchone()
            cursor.close()
            return agent
        return "feild to add mission!"
    
    def risk_level_calculation(self, data:dict):
        if 0 > data["difficulty"] or data["difficulty"] > 10 or 0 > data["importance"] or data["importance"] > 10:
            return None
        risk = data['difficulty'] * 2 + data['importance']
        if risk < 10:
            return 'LOW'
        elif risk < 17:
            return "MEDIUM"
        elif risk < 25:
            return "HIGH"
        else:
            return "CRITICAL"
        
    def get_all_mission(self):
        cursor = self.connction.cursor()
        cursor.execute("SELECT * FROM missions")
        missions = cursor.fetchall()
        cursor.close()
        return missions

    def get_mission_by_id(self, id:int):
        cursor = self.connction.cursor()
        cursor.execute("SELECT * FROM missions WHERE id=%s", (id,))
        agent = cursor.fetchall()
        cursor.close()
        if agent:
            return agent
        else:
            return None
        
    def assign_mission(self, id_m:int, id_a:int):
        agent = AgentDB().get_agent_by_id(id=id_a)
        if not agent:
            return f"not agent by {id} id"
        mission = self.get_mission_by_id(id=id_m)
        if not mission:
            return f"no mission by {id} id"
        
        if mission['risk_level'] == "CRITICAL":
            if agent['agent_renk'] != 'Commander':
                return "You cannot assign a critical mission to an agent below the rank of Commander."
        cursor = self.connction.cursor()
        cursor.execute("UPDATE missions SET status=ASSIGNED, assigned_agent_it=%s", (id,))
        self.connction.commit()

        change = cursor.rowcount > 0

        cursor.close()

        if change:
            return "mission assigned"
        else:
            return "mission ant assigned"
        
    def update_mission_status(self, id_m:int, status:str):
        if status not in ["IN_PROGRESS", "COMPLETED", "FAILED", "CANCELLED"]:
            return "status unknown"
        mission = self.get_mission_by_id(id_m)
        if not mission:
            return f"no mission by {id} id"
        cursor = self.connction.cursor()

        cursor.execute("UPDATE mission SET status=%s WHERE id=%s",(status,id_m))

        self.connction.commit()

        change = cursor.rowcount > 0
        cursor.close()
        if change:
            return "status update"
        else:
            return "status not update"

    def get_mission_by_id(self, id):
        
        


m = missionDB()
print(m.create_mission({"title" : "aaa", "description": "bbbb", "location": "ccc", "difficulty": 111, "importance": 11}))