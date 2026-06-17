from db_connection import db
from config import Creat_agents, Update_agents


class AgentDB:
    def __init__(self):
        self.connction = db.get_connection()

    def create_agent(self, data:Creat_agents):
        set_a = [key for key in data.keys()]
        set_b = " ,".join(set_a)

        val = tuple(data.values())

        cursor = self.connction.cursor()

        sql = f"INSERT INTO agents ({set_b}) VALUES (%s, %s, %s)"
        cursor.execute(sql, val)
        self.connction.commit()
   
        if cursor.rowcount > 0:
            id = cursor.lastrowid
            cursor.execute(f"SELECT * FROM agents WHERE id={id}")
            agent = cursor.fetchone()
            cursor.close()
            return agent
        return "feild to add agent!"

    def get_all_agents(self):
        curor = self.connction.cursor()
        curor.execute("SELECT * FROM agents")
        agents = curor.fetchall()
        curor.close()
        return agents
    
    def get_agent_by_id(self,id):
        cursor = self.connction.cursor()
        cursor.execute("SELECT * FROM agents WHERE id=%s", (id,))
        agent = cursor.fetchone()
        if agent:
            return agent
        else:
            return None
        
    def update_agent(self, id, data: Update_agents):
        set_a = [f"{key}=%s" for key in data.keys()]
        set_b = ", ".join(set_a)
        
        cursor = self.connction.cursor()

        sql = f"UPDATE agents SET {set_b} WHERE id=%s"
        val = list(data.values()) + [id]

        cursor.execute(sql, val)

        self.connction.commit()

        change = cursor.rowcount > 0
        cursor.close()

        if change:
            return f"agent {id} update"
        else:
            return f"no agent by id {id} or not change commit"

    def deactivate_agent(self,id):
        cursor = self.connction.cursor()
        cursor.execute("UPDATE agents SET is_active=False WHERE id=%s",(id,))
        self.connction.commit()
        change = cursor.rowcount > 0
        cursor.close()
        if change:
            return f"agent {id} deactivate"
        else:
            return f"not agent active by {id} id"
        
    def incrment_completed(self, id):
        cursor = self.connction.cursor()

        cursor.execute("UPDATE agents SET completed_mission=completed_mission + 1 WHERE id=%s", (id,))
        self.connction.commit()

        change = cursor.rowcount > 0
        cursor.close()
        if change:
            return f"add 1 completed mission to agent {id}"
        else:
            return f"no agent by {id} id"
        
    def incrment_failed(self, id):
        cursor = self.connction.cursor()

        cursor.execute("UPDATE agents SET failed_mission=failed_mission + 1 WHERE id=%s", (id,))
        self.connction.commit()

        change = cursor.rowcount > 0
        cursor.close()
        if change:
            return f"add 1 failed mission to agent {id}"
        else:
            return f"no agent by {id} id"
        
    def get_agent_performance(self, id):
        cursor = self.connction.cursor()
        cursor.execute("SELECT completed_mission, failed_mission FROM agents WHERE id=%s",(id,))

        data = list(cursor.fetchone())
        cursor.close()
        if not data:
            return f"no agent by {id} id"

        performance = {}
        performance['mission complit'] = data[0]
        performance['mission failed'] = data[1]
        performance['total'] = data[0] + data[1]
        performance['success_rate'] = data[0] * 100 / performance['total'] 

        return performance
    
    def count_active_agents(self):
        cursor = self.connction.cursor()

        cursor.execute("SELECT COUNT(*) FROM agents WHERE is_active=TRUE")
        agents = list(cursor.fetchone())
        cursor.close()

        if agents:
            return int(agents[0])
        else:
            return "no active agents"    


