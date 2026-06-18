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
        cursor = self.connction.cursor(dictionary=True)
        
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
        cursor = self.connction.cursor(dictionary=True)
        cursor.execute("SELECT * FROM missions")
        missions = cursor.fetchall()
        cursor.close()
        return missions

    def get_mission_by_id(self, id:int):
        cursor = self.connction.cursor(dictionary=True)
        cursor.execute("SELECT * FROM missions WHERE id=%s", (id,))
        mission = cursor.fetchone()
        cursor.close()
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

        cursor.execute("UPDATE missions SET status=%s WHERE id=%s",(status, id_m))

        self.connction.commit()

        change = cursor.rowcount > 0
        cursor.close()
        if change:
            return "status update"
        else:
            return None

    def get_open_missions_by_agent(self, id):
        cursor = self.connction.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) FROM missions WHERE assigned_agent_it=%s AND status='PROGRESS_IN'",(id,))
        countr = cursor.fetchone()
        cursor.close()
        print(countr['COUNT(*)'])
        return countr['COUNT(*)']
    
    def count_by_status(self, status):
        cursor = self.connction.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) FROM missions WHERE status=%s", (status,))
        stt = cursor.fetchone()
        cursor.close()
        return stt['COUNT(*)']
    
    def count_open_missions(self):
        cursor= self.connction.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) FROM missions WHERE status='ASSIGNED' OR status='PROGRESS_IN'")
        opens = cursor.fetchone()
        cursor.close()
        return {opens['COUNT(*)']}
     
    def count_critical_missions(self):
        cursor = self.connction.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) FROM missions WHERE risk_level='CRITICAL'")
        criti = cursor.fetchone()
        cursor.close()
        return {criti['COUNT(*)']}
    
    def get_top_agent(self):
        cursor = self.connction.cursor(dictionary=True)
        cursor.execute("SELECT * FROM agents ORDER BY completed_mission DESC LIMIT 1")
        top = cursor.fetchone()
        cursor.close()
        return top