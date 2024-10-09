import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from config import load_config
from handlers import register_handlers
from redis.asyncio import Redis 

async def check_price_alerts(bot: Bot):
    while True:
        from database.dynamodb import get_all_price_alerts, delete_price_alert
        alerts = await get_all_price_alerts()

        if not alerts:
            await asyncio.sleep(300) 
            continue

        currencies = list(set(alert['currency'] for alert in alerts))
        print(currencies)
        

        from services.crypto_api import get_crypto_price
        prices = await get_crypto_price([currency.lower() for currency in currencies], ['usd'])
        print(prices)


        for alert in alerts:
            user_id = alert['user_id']
            currency = alert['currency']
            target_price = float(alert['price'])
            current_price = prices.get(currency.lower(), {}).get('usd')

            if current_price is not None and current_price >= target_price:

                await bot.send_message(user_id, f"🚀 {currency} достиг цены ${current_price}!")


                await delete_price_alert(user_id, currency, target_price)

        await asyncio.sleep(100) 

async def main():
    config = load_config()

    redis = Redis(host=config.redis.host, port=config.redis.port)
    storage = RedisStorage(redis)
    bot = Bot(token=config.bot.token, default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher(storage=storage)

    register_handlers(dp)
    
    asyncio.create_task(check_price_alerts(bot))
    
    try:
        await dp.start_polling(bot)
    finally:
        await redis.aclose() 
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())