from aiogram import Dispatcher
from . import registration
from . import monitoring
from . import transactions
from . import alerts
from . import conversion
from . import help

def register_handlers(dp: Dispatcher):
    dp.include_router(registration.router)
    dp.include_router(monitoring.router)
    dp.include_router(transactions.router)
    dp.include_router(alerts.router)
    dp.include_router(conversion.router)
    dp.include_router(help.router)
    