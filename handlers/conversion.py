from aiogram import Router, types
from aiogram.filters import Command
from services.conversion import convert_currency

router = Router()

@router.message(Command("convert"))
async def cmd_convert(message: types.Message):
    args = message.text.split()
    if len(args) != 4:
        await message.answer("Используйте формат команды: /convert <сумма> <из валюты> <в валюту>")
        return

    amount = float(args[1])
    from_currency = args[2].upper()
    to_currency = args[3].upper()

    result = await convert_currency(amount, from_currency, to_currency)
    await message.answer(f"{amount} {from_currency} = {result} {to_currency}")
