from database.db_connection import db
from database.agent_db import AgentDB
from database.config import risk_level_calculation

class MissionDB:
    def __init__(self):
        self.connction = db.get_connection()

    def create_mission(self, data:dict):
        risk = risk_level_calculation(data)
        
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
        return None
    

    def get_all_mission(self):
        cursor = self.connction.cursor()
        cursor.execute("SELECT * FROM missions")
        missions = cursor.fetchall()
        cursor.close()
        return missions

    def get_mission_by_id(self, id:int):
        cursor = self.connction.cursor()
        cursor.execute("SELECT * FROM missions WHERE id=%s", (id,))
        mission = cursor.fetchone()
        cursor.close()
        print(mission)
        if mission:
            return mission
        else:
            return None
        
    def assign_mission(self, id_m:int, id_a:int):
    
        cursor = self.connction.cursor()
        cursor.execute("UPDATE missions SET status='ASSIGNED', assigned_agent_it=%s WHERE id=%s", (id_a, id_m))
        self.connction.commit()

        change = cursor.rowcount > 0

        cursor.close()

        if change:
            return "mission assigned"
        else:
            return None
        
    def update_mission_status(self, id_m:int, status:str):
    
        cursor = self.connction.cursor()

        cursor.execute("UPDATE missions SET status=%s WHERE id=%s",(status,id_m))

        self.connction.commit()

        change = cursor.rowcount > 0
        cursor.close()
        if change:
            return "status update"
        else:
            return None

        
    def count_open_mission(self, id:int):
        cursor = self.connction.cursor()
        cursor.execute("SELECT COUNT(*) FROM missions WHERE id=%s", (id,))
        countr = cursor.fetchone()
        cursor.close()
        return countr