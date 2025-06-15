# TelegramBot

Aiogram 3 + FastAPI + SQLite (async).  
Команды:  
- `/add_task` — добавить задачу  
- `/show_tasks` — список  
- `/delete_task` — удалить

## терминал Windows power shell

# server
- cd server
- python -m venv venv
- .\venv\Scripts\Activate.ps1 
- pip install -r requirements.txt
- uvicorn main:app --reload

# bot
- cd ../bot
- python -m venv venv
- #Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned - если ps1 блокируется
- .\venv\Scripts\Activate.ps1
- pip install -r requirements.txt
- cp .env.example .env          # вставьте свой BOT_TOKEN
- python main.py
