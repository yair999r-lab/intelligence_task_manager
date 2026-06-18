# Purpose of the system

The system is designed to manage agents and tasks.

The system can create agents and tasks and assign tasks to appropriate agents - according to risk level = rank.

The system creates a connection to the database where it stores the data and is responsible for retrieving and inserting the data.

The system is powered by a fastapi server - the list of "addresses" is attached below.

# File structure

intelligence-task-manager/
├── database/ 
│   ├── db_connection.py
│   ├── agent_db.py
│   └── mission_db.py
|── config.py
├── README.md
├── requirements.txt
└── .gitignore


# Table structure
## Agents table

id: AUTO_INCREMENT - Primary key
name: VARCHAR - NOT NULL
specialty: VARCHAR - NOT NULL
is_active: BOLLEAN - DEFAULT TRUE
completed missions: int - DEFAULT 0
failed missions: int - DEFAULT 0
agent rank - ENUM - Junior / Senior / Commander only!

## missions table

id: AUTO_INCREMENT - Primary key
title: VARCHAR - NOT NULL
description: TEXT - NOT NULL
location: VARCHAR - NOT NULL 
difficulty: INT - NOT NULL - Between 1 -10 only
importance: INT - NOT NULL - Between 1 -10 
status: VARCHAR - DEFAULT NEW
risk level: VARCHAR - Automatically calculated by formula
assigned agent id: INT - DEFAULT NULL 

# System structure

## Class DB_connection

### Methods

#### get_connection

the Method returns an active connection to the database

#### create database

The method creates a database if it does not exist

#### create tables 

The method creates the tables if they do not exist

## Class AgentDB

the class Using a connection created for me by the department

### Methods

#### create agent

Input: Dictionary with data
Action: Creates a new agent in the system,   
 returns: Dictionary of the new agent

#### get all agents

Returns: List of all agents - Empty list if there are no agents 

#### get agent by id

Input: id of the requested agent
Returns: The requested agent - None uf not exists 

#### update agent

Input: Dictionary of the update information, ID of the requested agent
Action: Updates the fields submitted in the system, returns: Success or error message

#### deactivate agent

Input: id of the requested agent
Action: Sets agent to inactive  
Returns: Success or error message

#### increment completed

Input: id of the requested agent
Action: Increases the number of completed tasks by 1  
Returns: Success or error message

#### increment failed

Input: id of the requested agent
Action: Increases the number of #### increment_failed
 tasks by 1      
 Returns: Success or error message

#### get agent performance

Input: id of the requested agent
Returns: A dictionary with agent execution data or an error message if agent does not exist.

#### count active agents

Returns: Number of active agents

## Class missionDB

the class Using a connection created for me by the department

### Methods

#### create_mission

Input: Dictionary of the new task information
Action: Creates a new task in the system,  
returns: the new task

#### get_all_missions

Returns: all tasks - empty list if no tasks exist

#### get_mission_by_id

Input: ID of the requested task
Returns: the requested task - None if no such task exists

#### assign_mission

Input: ID of the requested task and ID of the requested agent
Action: Assigning an action to an agent   
 returns: Success or error message

#### update_mission_status

Input: The required status, ID of the requested task
Action: Updates status of the requested task,   
returns: success or error message

#### get_open_missions_by_agent

Input: ID of the requested agent
Returns: Active or assigend tasks of the requested agent

#### count_all_missions

Returns: Total number of tasks

#### count_by_statut

Input: The requested status
Returns: Number of tasks with the requested status

#### count_open_missions

Returns: Number of open tasks

#### count_critical_missions

Returns: Number of critical tasks

#### get_top_agent

Returns: Agent with the most completed missions

# System rules

1. Rank must be Junior / Senior / Commander - any other value throws an error

2. Difficulty and importance must be between 1 and 10 — otherwise an error.

3. Risk level is calculated automatically when creating a task — the user does not submit it.

4. An agent with is_active=False cannot accept tasks.

5. An agent cannot have more than 3 open tasks (ASSIGNED / IN_PROGRESS) at the same time.

6. If risk level=CRITICAL — only an agent with the rank of Commander can accept the mission.

7. Only a task with a status of NEW can be assigned. After assignment: status=ASSIGNED.

8. Only a task with the status ASSIGNED can be started. After: status=IN_PROGRESS.

9. Only a task can be completed. IN_PROGRESS and changed to failed or completed status.

10. Only a task with a status of NEW or ASSIGNED can be canceled — otherwise an error.

# Running instructions

docker run -d --name intelligence-mysql -e MYSQL_ROOT_PASSWORD=1234 \
  -e MYSQL_DATABASE=Intelligence_db -p 3306:3306 mysql:8.0

# Endpoints

## missions endpoints

POST /mission - create mission
GET /mission - show all mission
GET /mission/{id} - show mission by id 
PUT /mission/{id}/assige/{agent_id} - assign mission to agent
PUT /missiion/{id}/start - start mission
PUT /mission/{id}/complete - complete mission 
PUT /mission/{id}/fail - mission falid
PUT /mission//{id}/cancel - mission canael

## agents endpoints

POST /agents - create agent
GET /agents - show all agents
GET /agents/{id} - show agent by id
PUT /agents/{id} - update agent
PUT /agents/{id}/deactivate - deactivate agent
PUT /agents/{id}/perpormance - show agent perpormance

## reports endpoints

GET /reports/summaty - General report
GET /reports/mission-by-status - Showing how many hits each status has 
GET /reports/top-agent - show top agent-Most completed tasks


# System flow

### Create an agent/task
User submits data to create a new task agent
The system verifies that the input is valid and meets the system requirements.
If correct - information about the new agent/task is returned and saved in our database.
If it is not correct, the system returns an error message to the customer and to us as well.

### Assign a task to an agent.

The client sends an ID of the requested task and the ID of the agent it wants to associate with it.

The system verifies that the agent exists. That the task exists. And that it can be assigned.

If so, the system updates our database that the task has been sent and the customer receives a success message.

If it is not possible to assign - the task is already assigned or has been canceled. Either the agent is inactive, or he does not have a level for importance, or he already has many tasks - the system does not update and returns a clear message to the customer.

The system is started by the main file - the command is attached below - and a connection to the database is created as long as our server is online and the connection is automatically closed when the server is shut down.

We have an app.log file saved in our system, which lists all actions - successes, errors, etc. - detailed with times.

# Running the system

The run command is: uvicorn main:app
Run the command in the terminal in the main folder