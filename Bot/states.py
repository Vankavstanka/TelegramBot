from aiogram.fsm.state import State, StatesGroup

class AddTask(StatesGroup):
    name = State()
    deadline = State()
