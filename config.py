import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class BotConfig:
    token: str

@dataclass
class RedisConfig:
    host: str
    port: int

@dataclass
class DynamoDBConfig:
    endpoint_url: str
    region_name: str

@dataclass
class Config:
    bot: BotConfig
    redis: RedisConfig
    dynamodb: DynamoDBConfig

def load_config():
    return Config(
        bot=BotConfig(
            token=os.getenv('BOT_TOKEN')
        ),
        redis=RedisConfig(
            host=os.getenv('REDIS_HOST'),
            port=int(os.getenv('REDIS_PORT', 6379))
        ),
        dynamodb=DynamoDBConfig(
            endpoint_url=os.getenv('DYNAMODB_ENDPOINT_URL'),
            region_name=os.getenv('AWS_REGION', 'us-east-1')
        )
    )
