import aiohttp

API_URL = 'https://open.er-api.com/v6/latest/USD'

async def get_fiat_rates():
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL) as response:
            return await response.json()