from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Начать тест"),KeyboardButton(text="Список вопросов")]
],
                                resize_keyboard=True,
                                input_field_placeholder="Выберите пункт меню")


answer_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='A',callback_data='answer_A'),InlineKeyboardButton(text='B',callback_data='answer_B')],
    [InlineKeyboardButton(text='C',callback_data='answer_C'),InlineKeyboardButton(text='D',callback_data='answer_D')],
    [InlineKeyboardButton(text='Завершить тестирование',callback_data='end_test')]
])

full_statistic = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Подробнее",callback_data="full_statistic")]
])

next_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Дальше", callback_data="next_question")]
])
