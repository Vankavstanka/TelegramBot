import asyncio, logging
from datetime import datetime

from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.client.default import DefaultBotProperties

from config import get_settings
from states import AddTask
import api_client, keyboards

logging.basicConfig(level=logging.INFO)

settings = get_settings()
bot = Bot(
    token=settings.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode="HTML")
)

dp = Dispatcher()
router = Router()
dp.include_router(router)

DATE_FORMAT = "%d.%m.%Y"

def _format_task(t: dict) -> str:
    return f"<b>{t['name']}</b> (дедлайн: {t['deadline']}, id={t['id']})"

WELCOME_TEXT = (
    "Привет! Я помогу вести список задач с дедлайнами:\n"
    "/add_task  /show_tasks  /delete_task"
)
NEXT_TEXT = (
    "Выбери следующее действие:\n"
    "/add_task  /show_tasks  /delete_task"
)

async def send_menu(chat, *, kind: str = "next"):
    text = WELCOME_TEXT if kind == "welcome" else NEXT_TEXT
    target = chat if isinstance(chat, Message) else chat.message
    await target.answer(text)

# handlers
@router.message(Command("start"))
async def cmd_start(msg: Message):
    await send_menu(msg, kind="welcome")

@router.message(Command("show_tasks"))
async def cmd_show(msg: Message):
    tasks = await api_client.get_tasks()
    if not tasks:
        await msg.answer("Нет задач")
    else:
        lines = [
        f"{i + 1}. <b>{t['name']}</b> (дедлайн: {t['deadline']})"
        for i, t in enumerate(tasks)
    ]
        await msg.answer("\n".join(lines))
    await send_menu(msg)

@router.message(Command("add_task"))
async def cmd_add(msg: Message, state: FSMContext):
    await msg.answer("Введите название задачи:")
    await state.set_state(AddTask.name)

@router.message(AddTask.name)
async def add_name(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text.strip())
    await msg.answer("Введите дедлайн (ДД.ММ.ГГГГ):")
    await state.set_state(AddTask.deadline)

@router.message(AddTask.deadline)
async def add_deadline(msg: Message, state: FSMContext):
    deadline = msg.text.strip()
    # проверка формата даты
    try:
        datetime.strptime(deadline, DATE_FORMAT)
    except ValueError:
        await msg.answer("Неправильный формат. Попробуйте ещё раз (ДД.ММ.ГГГГ).")
        return
    data = await state.get_data()
    await api_client.add_task(data["name"], deadline)
    await msg.answer("Задача добавлена.")
    await state.clear()
    await send_menu(msg)

@router.message(Command("delete_task"))
async def cmd_delete(msg: Message):
    tasks = await api_client.get_tasks()
    if not tasks:
        await msg.answer("Нет задач")
        return
    kb = keyboards.delete_keyboard(tasks)
    await msg.answer("Выберите задачу для удаления:", reply_markup=kb.as_markup())

@router.callback_query(F.data.startswith("del:"))
async def cb_delete(query: CallbackQuery):
    task_id = int(query.data.split(":")[1])
    await api_client.delete_task(task_id)
    await query.answer("Удалено.")
    # обновляем клавиатуру
    tasks = await api_client.get_tasks()
    if tasks:
        kb = keyboards.delete_keyboard(tasks)
        await query.message.edit_reply_markup(reply_markup=kb.as_markup())
    else:
        await query.message.edit_text("Все задачи удалены")
    await send_menu(query)

# запуск
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
