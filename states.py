from aiogram.fsm.state import State, StatesGroup


class StateUser(StatesGroup):
    contact = State()
    