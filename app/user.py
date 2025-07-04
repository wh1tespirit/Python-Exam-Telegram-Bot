from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
import app.keyboards as kb
from app.questions import load_questions_from_json
from aiogram.fsm.context import FSMContext
from app.states import Quiz
from asyncio import sleep

user = Router()

questions = load_questions_from_json("data/questions.json")

@user.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Добро пожаловать!',reply_markup=kb.main)

@user.message(F.text == "Начать тест")
async def start_test(message: Message, state: FSMContext):
    current_state = await state.get_state()

    # Если тест уже идёт — не запускаем новый
    if current_state == Quiz.in_quiz.state:
        await message.answer("❗ Вы уже проходите тест. Завершите его, прежде чем начинать новый.")
        return

    await state.set_data({"current_index": 0, "score": 0,"is_right":{}})
    await state.set_state(Quiz.in_quiz)

    data = await state.get_data()
    #await state.update_data(is_right = {data["current_index"]:None})

    question_index = data["current_index"]
    question = questions[question_index]
    letter = ['A', 'B', 'C', 'D']
    options = "\n".join([f"{letter[i]}) {opt}" for i, opt in enumerate(question['options'])])

    await message.answer(
        f"Вопрос {question_index + 1}/{len(questions)}:\n\n"
        f"{question['question']}\n\n"
        f"{options}",
        reply_markup=kb.answer_keyboard
    )



@user.callback_query(F.data.startswith('answer_'))
async def is_right(callback: CallbackQuery, state: FSMContext):
    await callback.answer()  # закрыть "часики"
    data = await state.get_data()

    index = data["current_index"]
    score = data["score"]
    user_answer = callback.data.split("_")[1]  # A, B, C, D
    correct_answer = questions[index]["correct"]
    question = questions[index]
    letter = ['A', 'B', 'C', 'D']
    options = "\n".join([f"{letter[i]}) {opt}" for i, opt in enumerate(question['options'])])

    base_text = (
        f"Вопрос {index + 1}/{len(questions)}:\n\n"
        f"{question['question']}\n\n"
        f"{options}"
    )

    # Показываем результат текущего вопроса
    if user_answer == correct_answer:
        feedback = "\n\n✅ Правильно!"
        score += 1
        data["is_right"][index+1] = '✅'
    else:
        feedback = f"\n\n❌ Неверно! Правильный ответ: {correct_answer}"
        data["is_right"][index+1] = '❌'
    
    # Если вопросов больше нет — завершить
    if index + 1 >= len(questions):
        await callback.message.edit_text(
            f"Тест завершён!\n\nВы правильно ответили на {score} из {len(questions)} вопросов.",
            reply_markup=kb.full_statistic
        )
        return

    # Показываем результат и кнопку "Дальше"
    await callback.message.edit_text(
        base_text + feedback,
        reply_markup=kb.next_keyboard
    )
    
    # Сохраняем данные для следующего вопроса
    await state.update_data(current_index=index, score=score)

@user.callback_query(F.data == "next_question")
async def next_question(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    index = data["current_index"] + 1
    
    next_question = questions[index]
    letter = ['A', 'B', 'C', 'D']
    options = "\n".join([f"{letter[i]}) {opt}" for i, opt in enumerate(next_question['options'])])
    next_text = (
        f"Вопрос {index + 1}/{len(questions)}:\n\n"
        f"{next_question['question']}\n\n"
        f"{options}"
    )

    await callback.message.edit_text(
        next_text,
        reply_markup=kb.answer_keyboard
    )
    
    await state.update_data(current_index=index)

@user.callback_query(F.data == "end_test")
async def ending_test(callback : CallbackQuery, state: FSMContext):
    await state.set_state()
    data = await state.get_data()
    score = data["score"]
    await callback.answer("")
    await callback.message.edit_text(f"Тест завершён!\n\nВы правильно ответили на {score} из {len(questions)} вопросов.",reply_markup=kb.full_statistic)

@user.callback_query(F.data == "full_statistic")
async def full_stat(callback : CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.answer("")
    result = '\n'.join(f"{k} : {v}" for k, v in data["is_right"].items())
    await callback.message.edit_text(f"{result}")
    await state.clear()  # Очищаем состояние после использования данных

@user.message(Quiz.in_quiz)
async def ignore_messages(message: Message):
    await message.answer("Пожалуйста, используйте кнопки для ответов.")

@user.message(F.text == "Список вопросов")
async def show_questions(message: Message):
    text = "\n".join([f"{i+1}. {q['question']}" for i, q in enumerate(questions)])
    await message.answer(text)