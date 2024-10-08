from aiogram.fsm.state import StatesGroup, State


class CertificateState(StatesGroup):
    fullname = State()
    picture = State()


class SearchState(StatesGroup):
    full_name = State()
