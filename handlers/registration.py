from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()

class RegistrationForm(StatesGroup):
    name = State()
    wallet = State()

@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("Привет! Как тебя зовут?")
    await state.set_state(RegistrationForm.name)

@router.message(RegistrationForm.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Укажите адрес вашего криптокошелька.")
    await state.set_state(RegistrationForm.wallet)

@router.message(RegistrationForm.wallet)
async def process_wallet(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    name = user_data.get('name')
    wallet = message.text

    from database.dynamodb import save_user
    await save_user(user_id=message.from_user.id, name=name, wallet=wallet)

    await message.answer(f"Спасибо за регистрацию, {name}!")
    await state.clear()
