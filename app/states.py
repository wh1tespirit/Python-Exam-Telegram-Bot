from aiogram.fsm.state import StatesGroup, State

class Quiz(StatesGroup):
    in_quiz = State()
