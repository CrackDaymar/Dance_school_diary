from aiogram import Bot, Dispatcher, types, executor
import aiogram
from setting import API_TELEGRAMM_TOKEN, list_day_1, list_day_2, list_day_3, list_day_4, list_day_5, list_day_6, list_day_7, list_day_8, list_day_9, list_day_10, list_day_11, list_day_12
from whitelist import user_id
import asyncio
from loguru import logger
import os

bot = Bot(API_TELEGRAMM_TOKEN)
dp = Dispatcher(bot)
logger.add('register.log', format="{time} {message}",
           level='DEBUG', rotation="10KB", compression='zip')

# class Form(StatesGroup):
#     a = State() # Задаем состояние

# @dp.message_handler(commands=['start'])
# async def start(message: types.Message):
#     await bot.send_message(message.chat.id, 'Отправь свое сообщение:')
#     await Form().a.set() # Устанавливаем состояние

# @dp.message_handler(state=Form().A) # Принимаем состояние
# async def start(message: types.Message, state: FSMContext):
#     async with state.proxy() as proxy: # Устанавливаем состояние ожидания
#         A.a = message.text
#     await state.finish() # Выключаем состояние

def auth(func):

    async def wrapper(message):
        for id in user_id:
            if message['from']['id'] == id:
                return await func(message)
        return await message.reply("Access denied", reply=False)

    return wrapper

@dp.message_handler(commands = ['start'])
async def start_uses(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    add_training_bighole_button = types.KeyboardButton('/Додати тренування', callback_data = '/register')
    add_training_smallhole_button = types.KeyboardButton('Вивести тренування', callback_data = '/show_training')
    markup.add(add_training_bighole_button, add_training_smallhole_button)
    await bot.send_message(message.chat.id, 'Привіт, в цьому боті ви можете вказати свої тренування, '
                                            'щоб вони десь були зайняті'
                                            '\n Для початку запису спочатку треба зарееструватися, для цього введіть '
                                            'команду /register', reply_markup=markup)

# @dp.message_handler(text= ['Додати тренування'])
# @auth
# async def get_reg(message: types.Message):
#     markup_ = types.InlineKeyboardMarkup()
#     but_reg = types.KeyboardButton('/register')
#     markup_.add(but_reg)
#     await bot.send_message(message.chat.id, "натисніть кнопку щоб зарееструвати нове тренування" ,reply_markup=markup_)
#
#
# @dp.message_handler(commands = ['register'])
# async def register_users(message: types.Message):
#
#     await bot.send_message(message.chat.id, 'Дякую за реєстрацію, Слава Україні, очікуйте, коли Ваша інформація буде '
#                                             'перевірена, і ми занесемо Вас до списку')

@dp.message_handler(commands = ['додати'])
@auth
async def add_training(message: types.Message):
    logger.info(f'ID пользователя = {message.chat.id}, фамилия = {message.chat.last_name}, имя =  '
                f'{message.chat.first_name}, имя аккаунта =  {message.chat.username}')
    markup = types.InlineKeyboardMarkup()
    add_training_bighole_button = types.KeyboardButton('великий зал', callback_data = 'butt_big_hole')
    add_training_smallhole_button = types.KeyboardButton('малий зал', callback_data = 'butt_small_hole')
    markup.add(add_training_bighole_button, add_training_smallhole_button)
    await bot.send_message(message.chat.id, 'Пропишите дату', reply_markup=markup)



@dp.callback_query_handler(lambda c: c.data == 'butt_big_hole')
async def add_training_big_hole(call: types.callback_query):
    await bot.answer_callback_query(call.id)
    await bot.send_message(call.message.chat.id, 'На який місяць хочете зробити запис?')
    markup = types.InlineKeyboardMarkup()
    _1month = types.KeyboardButton('1', callback_data = '1_month_big')
    _2month = types.KeyboardButton('2', callback_data = '2_month_big')
    _3month = types.KeyboardButton('3', callback_data = '3_month_big')
    _4month = types.KeyboardButton('4', callback_data = '4_month_big')
    _5month = types.KeyboardButton('5', callback_data = '5_month_big')
    _6month = types.KeyboardButton('6', callback_data = '6_month_big')
    _7month = types.KeyboardButton('7', callback_data = '7_month_big')
    _8month = types.KeyboardButton('8', callback_data = '8_month_big')
    _9month = types.KeyboardButton('9', callback_data = '9_month_big')
    _10month = types.KeyboardButton('10', callback_data = '10_month_big')
    _11month = types.KeyboardButton('11', callback_data = '11_month_big')
    _12month = types.KeyboardButton('12', callback_data = '12_month_big')
    markup.add(_1month, _2month, _3month, _4month, _5month, _6month, _7month, _8month, _9month, _10month, _11month,
               _12month)
    await bot.send_message(call.message.chat.id, 'Виберіть місяць в який хочете додати тренування', reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == '1_month_big')
async def add_date(call: types.callback_query):
    await bot.send_message(call.message.chat.id, 'Пропишіть день та час, на який хочете поставити тренуванная'
                                                 '\n у форматі (день - числами) (час з хвилинами)')
    markup = types.InlineKeyboardMarkup(resize_keyboard = True)
    i=0
    for j in list_day_1:
        i+=1
        add = str(i)
        day = types.KeyboardButton(f'{str(i)}', callback_data = j)
        markup.add(day)
    await bot.send_message(call.message.chat.id, 'Виберіть день, на який хочете записатися', reply_markup=markup)




@dp.callback_query_handler(lambda c: c.data == '2_month_big')
async def add_date(call: types.callback_query):
    await bot.send_message(call.message.chat.id, 'Пропишіть день та час, на який хочете поставити тренуванная'
                                                 '\n у форматі (день - числами) (час з хвилинами)'
                                                 '\n на приклад [10 10:30]')

@dp.callback_query_handler(lambda c: c.data == '3_month_big')
async def add_date(call: types.callback_query):
    await bot.send_message(call.message.chat.id, 'Пропишіть день та час, на який хочете поставити тренуванная'
                                                 '\n у форматі (день - числами) (час з хвилинами)'
                                                 '\n на приклад [10 10:30]')

@dp.callback_query_handler(lambda c: c.data == '4_month_big')
async def add_date(call: types.callback_query):
    await bot.send_message(call.message.chat.id, 'Пропишіть день та час, на який хочете поставити тренуванная'
                                                 '\n у форматі (день - числами) (час з хвилинами)'
                                                 '\n на приклад [10 10:30]')

@dp.callback_query_handler(lambda c: c.data == '5_month_big')
async def add_date(call: types.callback_query):
    await bot.send_message(call.message.chat.id, 'Пропишіть день та час, на який хочете поставити тренуванная'
                                                 '\n у форматі (день - числами) (час з хвилинами)'
                                                 '\n на приклад [10 10:30]')

@dp.callback_query_handler(lambda c: c.data == '6_month_big')
async def add_date(call: types.callback_query):
    await bot.send_message(call.message.chat.id, 'Пропишіть день та час, на який хочете поставити тренуванная'
                                                 '\n у форматі (день - числами) (час з хвилинами)'
                                                 '\n на приклад [10 10:30]')

@dp.callback_query_handler(lambda c: c.data == '7_month_big')
async def add_date(call: types.callback_query):
    await bot.send_message(call.message.chat.id, 'Пропишіть день та час, на який хочете поставити тренуванная'
                                                 '\n у форматі (день - числами) (час з хвилинами)'
                                                 '\n на приклад [10 10:30]')

@dp.callback_query_handler(lambda c: c.data == '8_month_big')
async def add_date(call: types.callback_query):
    await bot.send_message(call.message.chat.id, 'Пропишіть день та час, на який хочете поставити тренуванная'
                                                 '\n у форматі (день - числами) (час з хвилинами)'
                                                 '\n на приклад [10 10:30]')

@dp.callback_query_handler(lambda c: c.data == '9_month_big')
async def add_date(call: types.callback_query):
    await bot.send_message(call.message.chat.id, 'Пропишіть день та час, на який хочете поставити тренуванная'
                                                 '\n у форматі (день - числами) (час з хвилинами)'
                                                 '\n на приклад [10 10:30]')

@dp.callback_query_handler(lambda c: c.data == '10_month_big')
async def add_date(call: types.callback_query):
    await bot.send_message(call.message.chat.id, 'Пропишіть день та час, на який хочете поставити тренуванная'
                                                 '\n у форматі (день - числами) (час з хвилинами)'
                                                 '\n на приклад [10 10:30]')

@dp.callback_query_handler(lambda c: c.data == '11_month_big')
async def add_date(call: types.callback_query):
    await bot.send_message(call.message.chat.id, 'Пропишіть день та час, на який хочете поставити тренуванная'
                                                 '\n у форматі (день - числами) (час з хвилинами)'
                                                 '\n на приклад [10 10:30]')

@dp.callback_query_handler(lambda c: c.data == '12_month_big')
async def add_date(call: types.callback_query):
    await bot.send_message(call.message.chat.id, 'Пропишіть день та час, на який хочете поставити тренуванная'
                                                 '\n у форматі (день - числами) (час з хвилинами)'
                                                 '\n на приклад [10 10:30]')

@dp.callback_query_handler(lambda c: c.data == 'butt_small_hole')
async def add_training_big_hole(call: types.callback_query):
    await bot.answer_callback_query(call.id)
    await bot.send_message(call.message.chat.id, 'На який місяць хочете зробити запис?')
    markup = types.InlineKeyboardMarkup()
    _1month = types.KeyboardButton('1', callback_data = '1_month_small')
    _2month = types.KeyboardButton('2', callback_data = '2_month_small')
    _3month = types.KeyboardButton('3', callback_data = '3_month_small')
    _4month = types.KeyboardButton('4', callback_data = '4_month_small')
    _5month = types.KeyboardButton('5', callback_data = '5_month_small')
    _6month = types.KeyboardButton('6', callback_data = '6_month_small')
    _7month = types.KeyboardButton('7', callback_data = '7_month_small')
    _8month = types.KeyboardButton('8', callback_data = '8_month_small')
    _9month = types.KeyboardButton('9', callback_data = '9_month_small')
    _10month = types.KeyboardButton('10', callback_data = '10_month_small')
    _11month = types.KeyboardButton('11', callback_data = '11_month_small')
    _12month = types.KeyboardButton('12', callback_data = '12_month_small')
    markup.add(_1month, _2month, _3month, _4month, _5month, _6month, _7month, _8month, _9month, _10month, _11month,
               _12month)
    await bot.send_message(call.message.chat.id, 'Виберіть місяць в який хочете додати тренування', reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == '1_month_small')
async def add_date(call: types.callback_query):
    await bot.send_message(call.message.chat.id, 'Пропишіть день та час, на який хочете поставити тренуванная'
                                                 '\n у форматі (день - числами) (час з хвилинами)'
                                                 '\n на приклад [10 10:30]')


@dp.callback_query_handler(lambda c: c.data == '2_month_small')
async def add_date(call: types.callback_query):
    await bot.send_message(call.message.chat.id, 'Пропишіть день та час, на який хочете поставити тренуванная'
                                                 '\n у форматі (день - числами) (час з хвилинами)'
                                                 '\n на приклад [10 10:30]')

@dp.callback_query_handler(lambda c: c.data == '3_month_small')
async def add_date(call: types.callback_query):
    await bot.send_message(call.message.chat.id, 'Пропишіть день та час, на який хочете поставити тренуванная'
                                                 '\n у форматі (день - числами) (час з хвилинами)'
                                                 '\n на приклад [10 10:30]')

@dp.callback_query_handler(lambda c: c.data == '4_month_small')
async def add_date(call: types.callback_query):
    await bot.send_message(call.message.chat.id, 'Пропишіть день та час, на який хочете поставити тренуванная'
                                                 '\n у форматі (день - числами) (час з хвилинами)'
                                                 '\n на приклад [10 10:30]')

@dp.callback_query_handler(lambda c: c.data == '5_month_small')
async def add_date(call: types.callback_query):
    await bot.send_message(call.message.chat.id, 'Пропишіть день та час, на який хочете поставити тренуванная'
                                                 '\n у форматі (день - числами) (час з хвилинами)'
                                                 '\n на приклад [10 10:30]')

@dp.callback_query_handler(lambda c: c.data == '6_month_small')
async def add_date(call: types.callback_query):
    await bot.send_message(call.message.chat.id, 'Пропишіть день та час, на який хочете поставити тренуванная'
                                                 '\n у форматі (день - числами) (час з хвилинами)'
                                                 '\n на приклад [10 10:30]')

@dp.callback_query_handler(lambda c: c.data == '7_month_small')
async def add_date(call: types.callback_query):
    await bot.send_message(call.message.chat.id, 'Пропишіть день та час, на який хочете поставити тренуванная'
                                                 '\n у форматі (день - числами) (час з хвилинами)'
                                                 '\n на приклад [10 10:30]')

@dp.callback_query_handler(lambda c: c.data == '8_month_small')
async def add_date(call: types.callback_query):
    await bot.send_message(call.message.chat.id, 'Пропишіть день та час, на який хочете поставити тренуванная'
                                                 '\n у форматі (день - числами) (час з хвилинами)'
                                                 '\n на приклад [10 10:30]')

@dp.callback_query_handler(lambda c: c.data == '9_month_small')
async def add_date(call: types.callback_query):
    await bot.send_message(call.message.chat.id, 'Пропишіть день та час, на який хочете поставити тренуванная'
                                                 '\n у форматі (день - числами) (час з хвилинами)'
                                                 '\n на приклад [10 10:30]')

@dp.callback_query_handler(lambda c: c.data == '10_month_small')
async def add_date(call: types.callback_query):
    await bot.send_message(call.message.chat.id, 'Пропишіть день та час, на який хочете поставити тренуванная'
                                                 '\n у форматі (день - числами) (час з хвилинами)'
                                                 '\n на приклад [10 10:30]')

@dp.callback_query_handler(lambda c: c.data == '11_month_small')
async def add_date(call: types.callback_query):
    await bot.send_message(call.message.chat.id, 'Пропишіть день та час, на який хочете поставити тренуванная'
                                                 '\n у форматі (день - числами) (час з хвилинами)'
                                                 '\n на приклад [10 10:30]')

@dp.callback_query_handler(lambda c: c.data == '12_month_small')
async def add_date(call: types.callback_query):
    await bot.send_message(call.message.chat.id, 'Пропишіть день та час, на який хочете поставити тренуванная'
                                                 '\n у форматі (день - числами) (час з хвилинами)'
                                                 '\n на приклад [10 10:30]')


def main():
    try:
        executor.start_polling(dp, skip_updates=True)
    except Exception as ex:
        logger.critical(f'ошибка = {ex}')


if __name__ == '__main__':
    main()