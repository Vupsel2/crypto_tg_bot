import boto3
from config import load_config
from boto3.dynamodb.conditions import Key
from decimal import Decimal

config = load_config()

dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url=config.dynamodb.endpoint_url,
    region_name=config.dynamodb.region_name
)

async def save_user(user_id, name, wallet):
    table = dynamodb.Table('Users')
    table.put_item(
        Item={
            'user_id': str(user_id),
            'name': name,
            'wallet': wallet
        }
    )

async def save_price_alert(user_id, currency, price):
    table = dynamodb.Table('PriceAlerts')
    currency_price = f"{currency}#{price}"
    table.put_item(
        Item={
            'user_id': str(user_id),
            'currency_price': currency_price,
            'currency': currency,
            'price': Decimal(str(price))
        }
    )

async def get_all_price_alerts():
    table = dynamodb.Table('PriceAlerts')
    response = table.scan()
    return response.get('Items', [])

async def delete_price_alert(user_id, currency, price):
    table = dynamodb.Table('PriceAlerts')
    currency_price = f"{currency}#{float(price)}"
    print(currency_price)
    print(Decimal(float(100.123)))
    table.delete_item(
        Key={
            'user_id': str(user_id),
            'currency_price': currency_price
        }
    )
    
async def get_user_price_alerts(user_id):
    table = dynamodb.Table('PriceAlerts')
    response = table.query(
        KeyConditionExpression=Key('user_id').eq(str(user_id))
    )
    return response.get('Items', [])