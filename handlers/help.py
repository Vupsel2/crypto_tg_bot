from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("help"))
async def help_command(message: types.Message):
    response = (
        "Доступные команды:\n"
        "/start - Начать работу с ботом\n"
        "/set_alert - Установить уведомление о достижении курса\n"
        "/my_alerts - Показать ваши активные уведомления\n"
        "/price - Показать текущие курсы основных криптовалют\n"
        "/help - Показать это сообщение\n"
    )
    await message.answer(response)