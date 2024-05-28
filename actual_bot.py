import logging
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
from setting import API_TELEGRAMM_TOKEN
from whitelist import user_id

logging.basicConfig(level=logging.INFO)

API_TOKEN = API_TELEGRAMM_TOKEN


bot = Bot(token=API_TOKEN)

# For example use simple MemoryStorage for Dispatcher.
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def get_teacher(curr_id):
    for id in user_id:
        if curr_id == id:
            return True
    return False


# States
class Form(StatesGroup):
    holl = State()  # Will be represented in storage as 'Form:name'
    date = State()  # Will be represented in storage as 'Form:age'
    time = State()  # Will be represented in storage as 'Form:time'
    teacher = State()  # Will be represented in storage as 'Form:teacher'


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


@dp.message_handler(commands='додати')
async def cmd_start(message: types.Message):
    """
    Conversation's entry point
    """
    # Set state
    await Form.holl.set()

    markup =types.ReplyKeyboardMarkup(resize_keyboard = True, selective = True)
    markup.add("Великий холл", "Малий холл")

    await message.reply("Привіт виберіть холл в який хочете додати тренування", reply_markup=markup)


@dp.message_handler(state=Form.holl)
async def get_holl(message: types.Message, state: FSMContext):
    # Update state and data
    await Form.next()
    await state.update_data(holl=message.text)
    print(message.text)

    await message.reply("На яку дату записати тренування?")


@dp.message_handler(state=Form.date)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(date=message.text)
    await Form.next()
    await message.reply("На какое время Вас записать?")


# Check age. Age gotta be digit
@dp.message_handler(state=Form.time)
async def process_age_invalid(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await state.update_data(time=message.text)
        data['time'] = message.text
        data['teacher'] = get_teacher(message.chat.id)

        # Remove keyboard
        markup = types.ReplyKeyboardRemove()

        # And send message
        await bot.send_message(
            message.chat.id, ('Дякую за запис, Ви записали тренування на дату :' + str(data['date']) +
                                '\n Час запису :' + str(data['time']) +
                                '\n Зал в якому відбудется тренування :' + str(data['holl'])+
                                '\n тренер який записав тренування :' + str(data['teacher']))
        )

    # Finish conversation
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)