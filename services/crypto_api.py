import aiohttp

API_URL = 'https://api.coingecko.com/api/v3/simple/price'

async def get_crypto_price(crypto_ids, vs_currencies):
    params = {
        'ids': ','.join(crypto_ids),
        'vs_currencies': ','.join(vs_currencies)
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL, params=params) as response:
            return await response.json()
