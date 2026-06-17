# Purpose of the system

The system is designed to manage agents and tasks.

The system can create agents and tasks and assign tasks to appropriate agents - according to risk level = rank.

The system creates a connection to the database where it stores the data and is responsible for retrieving and inserting the data.

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


