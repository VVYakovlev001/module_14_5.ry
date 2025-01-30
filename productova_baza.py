from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import fail
from crud_functions import add_user

api = "7345376595:AAHyZWBH1R5sP5J_lA4vACj1aJTG6dny2wI"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = KeyboardButton(text='Рассчитать')
button_2 = KeyboardButton(text='Информация')
button_3 = KeyboardButton(text="Купить")
button_4 = KeyboardButton(text="Регистрация")
kb.row(button_1)
kb.row(button_2)
kb.add(button_3)
kb.add(button_4)

kb2 = InlineKeyboardMarkup(resize_keyboard=True)
i_button_1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
i_button_2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb2.add(i_button_1)
kb2.add(i_button_2)

kb3 = InlineKeyboardMarkup(resize_keyboard=True)  #
i_button_3 = InlineKeyboardButton(text="Продукт 1", callback_data="product_buying")
i_button_4 = InlineKeyboardButton(text="Продукт 2", callback_data="product_buying")
i_button_5 = InlineKeyboardButton(text="Продукт 3", callback_data="product_buying")
i_button_6 = InlineKeyboardButton(text="Продукт 4", callback_data="product_buying")

kb3.add(i_button_3)
kb3.row(i_button_4)
kb3.row(i_button_5)
kb3.row(i_button_6)


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = 1000


@dp.message_handler(text="Регистрация")
async def sing_up(message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    await state.update_data(username=message.text)
    data = await state.get_data()
    i = (data['username'])
    if i is True:
        await state.update_data(username=message.text)
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()
    else:
        await message.answer("Пользователь существует, введите другое имя")
        await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    add_user(data['username'], data['email'], data['age'])
    await state.finish()


class UserState(StatesGroup):
    age = State()  # возраст
    growth = State()  # рост
    weight = State()  # вес


@dp.message_handler(commands=['start'])
async def starts(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.message_handler(text="Информация")
async def info(message):
    await message.answer("Я бот помогающий твоему здоровью,Если хотите рассчитать вашу "
                         "норму калорий - нажмите кнопку Рассчитать")


@dp.message_handler(text='Рассчитать')
async def menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb2)


@dp.callback_query_handler(text="formulas")
async def get_formulas(call):
    await call.message.answer('для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;'
                              'для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer("Введите свой возраст:")
    await UserState.age.set()
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def set_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    norm_calories_men = int(10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5)
    norm_calories_vomen = int(10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161)
    await message.answer(f"Мужская норма в сутки {norm_calories_men} ккал."
                         f" Женская норма в сутки {norm_calories_vomen} ккал.")
    await state.finish()


@dp.message_handler(text="Купить")
async def get_buying_list(message):
    for i in range(4):
        number = i + 1
        await message.answer(
            f"Название: {title}{number} | Описание: {description}{number} | Цена: {price}{number * 100}")
        with open(f'fail/{str(number)}kartinki.pip.jpg', 'rb') as img:
            await message.answer_photo(img)

        await message.answer(text='Выберете продукт для покупки:', reply_markup=kb3)


@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer(text="Вы успешно приобрели продукт!")
    await call.answer()


@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


# Упрощенный вариант формулы Миффлина - Сан Жеора:
# для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;
# для женщин: 10 х вес (кг) + 6,25 х рост (см) - 5 х возраст (г) -161
title = "Продукт"
description = "Описание"
price = "Цена"

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)


'''
Изменения в Telegram-бот:
Кнопки главного меню дополните кнопкой "Регистрация".
Напишите новый класс состояний RegistrationState с следующими объектами класса State:
 username, email, age, balance(по умолчанию 1000).
Создайте цепочку изменений состояний RegistrationState.
Фукнции цепочки состояний RegistrationState:
sing_up(message):
Оберните её в message_handler, который реагирует на текстовое сообщение 'Регистрация'.
Эта функция должна выводить в Telegram-бот сообщение "Введите имя пользователя
 (только латинский алфавит):".
После ожидать ввода имени в атрибут RegistrationState.username при помощи метода set.
set_username(message, state):
Оберните её в message_handler, который реагирует на состояние
 RegistrationState.username.
Если пользователя message.text ещё нет в таблице, то должны обновляться
 данные в состоянии username на message.text. Далее выводится сообщение
  "Введите свой email:" и принимается новое состояние RegistrationState.email.
Если пользователь с таким message.text есть в таблице, то выводить
 "Пользователь существует, введите другое имя" и запрашивать новое состояние для
  RegistrationState.username.
set_email(message, state):
Оберните её в message_handler, который реагирует на состояние RegistrationState.email.
Эта функция должна обновляться данные в состоянии RegistrationState.email на
 message.text.
Далее выводить сообщение "Введите свой возраст:":
После ожидать ввода возраста в атрибут RegistrationState.age.
set_age(message, state):
Оберните её в message_handler, который реагирует на состояние RegistrationState.age.
Эта функция должна обновляться данные в состоянии RegistrationState.age на
 message.text.
Далее брать все данные (username, email и age) из состояния и записывать в таблицу Users при помощи ранее написанной crud-функции add_user.
В конце завершать приём состояний при помощи метода finish().
Перед запуском бота пополните вашу таблицу Products 4 или более записями для
 последующего вывода в чате Telegram-бота.
'''
