from database.db_connection import db
 
class AgentDB:
    def __init__(self):
        self.connction = db.get_connection()
        

    def create_agent(self, data:dict):
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
        return None

    def get_all_agents(self):
        curor = self.connction.cursor(dictionary=True)
        curor.execute("SELECT * FROM agents")
        agents = curor.fetchall()
        curor.close()
        return agents
    
    def get_agent_by_id(self,id):
        cursor = self.connction.cursor(dictionary=True)
        cursor.execute("SELECT * FROM agents WHERE id=%s", (id,))
        agent = cursor.fetchone()
        if agent:
            return agent
        else:
            return None
        
    def update_agent(self, id:int, data: dict):
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
            return None

    def deactivate_agent(self,id):
        cursor = self.connction.cursor()
        cursor.execute("UPDATE agents SET is_active=False WHERE id=%s",(id,))
        self.connction.commit()
        change = cursor.rowcount > 0
        cursor.close()
        if change:
            return f"agent {id} deactivate"
        else:
            return None
        
    def incrment_completed(self, id):
        cursor = self.connction.cursor()

        cursor.execute("UPDATE agents SET completed_mission=completed_mission + 1 WHERE id=%s", (id,))
        self.connction.commit()

        change = cursor.rowcount > 0
        
        if change:
            cursor.execute("SELECT completed_mission FROM agents WHERE id=%s",(id,))
            completed = cursor.fetchone()
            cursor.close()
            return f"agent {id} heve {completed} completed mission"
        else:
            cursor.close()
            return None
        
    def incrment_failed(self, id):
        cursor = self.connction.cursor(dictionary=True)

        cursor.execute("UPDATE agents SET failed_mission=failed_mission + 1 WHERE id=%s", (id,))
        self.connction.commit()

        change = cursor.rowcount > 0
        cursor.close()
        if change:
            cursor.execute("SELECT failed_mission FROM agents WHERE id=%s",(id,))
            failed = cursor.fetchone()
            cursor.close()
            return f"agent {id} heve {failed} failed mission"
        else:
            cursor.close()
            return None
        
    def get_agent_performance(self, id):
        cursor = self.connction.cursor()
        cursor.execute("SELECT completed_mission, failed_mission FROM agents WHERE id=%s",(id,))

        data = cursor.fetchone()
        cursor.close()
        if not data:
            return None

        performance = {}
        performance['mission complit'] = data[0]
        performance['mission failed'] = data[1]
        performance['total'] = data[0] + data[1]
        performance["success_rate"] = 0
        if performance["total"] > 0:

            performance['success_rate'] = data[0] * 100 / performance['total'] 
        return performance
    
    def count_active_agents(self):
        cursor = self.connction.cursor(dictionary=True)

        cursor.execute("SELECT COUNT(*) FROM agents WHERE is_active=TRUE")
        agents = cursor.fetchall()
        cursor.close()

        return agents


