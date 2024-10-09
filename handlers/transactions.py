from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("transactions"))
async def show_transactions(message: types.Message):
    await message.answer("Ваши последние транзакции...")