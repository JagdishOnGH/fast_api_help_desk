depedency used:
    1. fastapi
    2. sqlalchemy
    3. alembic
    4. uvicorn
    5. passlib
    6. python-jose
    7. psycopg2
    
    for database
        1. postgresql
        2. pgadmin
    for secure hashing and signature
        1. passlib
        2. python-jose
    for database connection
        1. psycopg2
    setup instruction
    1. create a virtual environment
    2. activate the virtual environment venv
    3. install the required dependencies
    4. create a database
    5. run the migrations
    6. run the application
 
 put database credentials in .env file
 for dev: database.py has DATABASE_URL = ""


 alembic commands to generate and push migrations for new projects
    1. 
Purpose	Command
Initialize Alembic	alembic init alembic
Create New Migration Script	alembic revision --autogenerate -m "message"

Apply Latest Migrations	alembic upgrade head
Downgrade One Step	alembic downgrade -1
Check Current Revision	alembic current
Show Migration History	alembic history 

