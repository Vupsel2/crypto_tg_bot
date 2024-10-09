from aiogram import Router, types
from aiogram.filters import Command
from services.crypto_api import get_crypto_price

router = Router()

@router.message(Command("price"))
async def cmd_price(message: types.Message):
    crypto_prices = await get_crypto_price(['bitcoin', 'ethereum'], ['usd'])
    btc_price = crypto_prices.get('bitcoin', {}).get('usd',)
    eth_price = crypto_prices.get('ethereum', {}).get('usd',)
    await message.answer(f"Курс BTC: ${btc_price}\nКурс ETH: ${eth_price}")
