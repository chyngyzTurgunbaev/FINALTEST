from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, F, types
from config import db
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

survey_router = Router()


class BookSurvey(StatesGroup):
    name = State()
    age = State()
    occupation = State()
    salary = State()


@survey_router.message(Command("stop"))
@survey_router.message(F.text.lower() == "стоп")
async def stop(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Спасибо за прохождение опроса!")


# Опрос начался
@survey_router.callback_query(F.data == 'feedback')
async def start_review(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(BookSurvey.name)
    await call.message.answer("Здравствуйте! Как Вас зовут?")


@survey_router.message(BookSurvey.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько вам лет?")
    await state.set_state(BookSurvey.age)


@survey_router.message(BookSurvey.age)
async def process_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
    except ValueError:
        await message.answer("Пожалуйста, введите числовое значение возраста.")
        return

    if age < 17:
        await message.answer("Опрос предназначен только для лиц старше 17 лет. Спасибо за участие!")
        await state.clear()
    else:
        await state.update_data(age=age)
        await message.answer("Ваш род занятий?")
        await state.set_state(BookSurvey.occupation)


@survey_router.message(BookSurvey.occupation)
async def process_occupation(message: types.Message, state: FSMContext):
    await state.update_data(occupation=message.text)
    await message.answer("Ваша заработная плата?")
    await state.set_state(BookSurvey.salary)


@survey_router.message(BookSurvey.salary)
async def process_salary(message: types.Message, state: FSMContext):
    await state.update_data(salary=message.text)
    data = await state.get_data()
    with db:
        db.execute(
            '''INSERT INTO survey (name, age, occupation, salary) VALUES ( ?, ?, ?, ?)''',
            (message.from_user.id, data['name'], data['age'], data['occupation'], data['salary'])
        )
    await message.answer("Ваш отзыв успешно принят!")
    await state.clear()
