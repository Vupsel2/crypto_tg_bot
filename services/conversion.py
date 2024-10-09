from services.fiat_api import get_fiat_rates

async def convert_currency(amount, from_currency, to_currency):
    rates = await get_fiat_rates()
    rates = rates.get('rates', {})
    if from_currency not in rates or to_currency not in rates:
        return "Неверная валюта"

    from_rate = rates[from_currency]
    to_rate = rates[to_currency]

    converted_amount = amount / from_rate * to_rate
    return round(converted_amount, 2)
