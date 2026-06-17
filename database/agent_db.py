from db_connection import DB_connection


class AgentDB:
    def __init__(self):
        self.connection = DB_connection().get_connection()

    def create_agent(self, data:dict):
        set_a = [key for key in data.keys()]
        set_b = " ,".join(set_a)

        Placeholder = "%s," * len(data)
        print(set_b,Placeholder)

        val = list(data.values())
        print(val)

        sql = f"INSERT INTO agents ({set_b}) VALUES({Placeholder})"

        cursor = self.connection.cursor()
        cursor.execute(sql, val)
        self.connection.commit()

        if cursor.rowcount > 0:
            id = cursor.lastrowid
            cursor.execute(f"SELECT * FROM agents WHERE id={id}")
            agent = cursor.fetchone()
            cursor.close()
            return agent
        return {"messag:" "feild to add agent!"}

        

c = AgentDB()
c.create_agent({"name": "yair", "specialty": "read", "agent_renk": "Junior"})