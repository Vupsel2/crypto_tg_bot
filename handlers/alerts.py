from aiogram import Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters.callback_data import CallbackData
from decimal import Decimal
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F

router = Router()
class AlertCallbackData(CallbackData, prefix="alert"):
    action: str
    currency: str
    price: str

class CancelCallbackData(CallbackData, prefix="cancel"):
    action: str



class AlertStates(StatesGroup):
    waiting_for_currency = State()
    waiting_for_price = State()

@router.message(Command("set_alert"))
async def set_alert_command(message: types.Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Скасувати", callback_data=CancelCallbackData(action="cancel").pack())]
    ])
    
    await message.answer("Введіть символ криптовалюти (наприклад, bitcoin, ethereum):", reply_markup=keyboard)
    await state.set_state(AlertStates.waiting_for_currency)

@router.message(AlertStates.waiting_for_currency)
async def process_currency(message: types.Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Скасувати", callback_data=CancelCallbackData(action="cancel").pack())]
    ])
    currency = message.text
    from services.crypto_api import get_crypto_price
    check = await get_crypto_price([currency], ['usd'])
    if not check:
        await message.answer(f"Наразі криптовалюта '{currency}' не доступна, введіть іншу валюту", reply_markup=keyboard)
        return
    currency = currency.upper()
    await state.update_data(currency=currency)
    await message.answer(f"Введіть ціну в USD для встановлення сповіщення по {currency}:", reply_markup=keyboard)
    await state.set_state(AlertStates.waiting_for_price)

@router.message(AlertStates.waiting_for_price)
async def process_price(message: types.Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Скасувати", callback_data=CancelCallbackData(action="cancel").pack())]
    ])
    try:
        price = float(message.text)
    except ValueError:
        await message.answer("Будь ласка, введіть правильне число для ціни.", reply_markup=keyboard)
        return

    user_data = await state.get_data()
    currency = user_data['currency']

    from database.dynamodb import save_price_alert
    await save_price_alert(message.from_user.id, currency, price)

    await message.answer(f"Сповіщення встановлено: {currency} досягне {price}$")
    await state.clear()

@router.callback_query(CancelCallbackData.filter(F.action == "cancel"))
async def cancel_alert(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Додавання сповіщення скасовано.")


@router.message(Command(commands=["my_alerts"]))
async def show_my_alerts(message: types.Message):
    from database.dynamodb import get_user_price_alerts
    alerts = await get_user_price_alerts(message.from_user.id)
    
    if not alerts:
        await message.answer("Ви не маєте активних повідомлень.")
        return

    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Меню", callback_data="menu")
    keyboard_builder.button(text="Удалить", callback_data=AlertCallbackData(action="show_delete_menu",currency="", price="").pack())

    keyboard = keyboard_builder.as_markup()

    response = "Ваші активні сповіщення:\n"
    for alert in alerts:
        response += f"- {alert['currency']} при ціні ${alert['price']}\n"

    await message.answer(response, reply_markup=keyboard)


@router.callback_query(AlertCallbackData.filter(F.action == "show_delete_menu"))
async def show_delete_menu(query: types.CallbackQuery, callback_data: AlertCallbackData):
    
    from database.dynamodb import get_user_price_alerts
    alerts = await get_user_price_alerts(query.from_user.id)

    if not alerts:
        await query.message.answer("Немає активних сповіщень")
        return

    keyboard_builder = InlineKeyboardBuilder()

    for alert in alerts:
        button_text = f"🗑 Видалити {alert['currency']} по ціні ${alert['price']}"
        callback_data = AlertCallbackData(
            action="delete",
            currency=alert['currency'],
            price=str(alert['price'])
        ).pack()
        keyboard_builder.button(text=button_text, callback_data=callback_data)
    keyboard_builder.button(text="Скасувати", callback_data=AlertCallbackData(action="cancel_delete", currency="", price="").pack())

    keyboard = keyboard_builder.adjust(1).as_markup()

    await query.message.edit_text("Виберіть повідомлення для видалення:", reply_markup=keyboard)

@router.callback_query(AlertCallbackData.filter(F.action == "delete"))
async def delete_alert_callback(query: types.CallbackQuery, callback_data: AlertCallbackData):
    from database.dynamodb import delete_price_alert

    currency = callback_data.currency
    price = callback_data.price

    await delete_price_alert(query.from_user.id, currency, price)

    await query.message.edit_text(f"Повідомлення про {currency} при ціні ${price} було видалено.",reply_markup=None)

    
