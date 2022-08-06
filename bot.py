from aiogram.contrib.fsm_storage.memory import MemoryStorage

from business import add_date
from config import TELEGRAM_TOKEN
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton,\
    InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.dispatcher import FSMContext
from main import get_group_list, get_sql_class_time_list, get_teacher_list, get_schedule_teacher, create_new_group, \
    create_new_user
from stategroup import GroupStatesGroup, UserStatesGroup

bot = Bot(token=TELEGRAM_TOKEN)  # Объект бота
dp = Dispatcher(bot,
                storage=MemoryStorage())  # Диспетчер для бота
logging.basicConfig(level=logging.INFO)  # Включаем логирование, чтобы не пропустить важные сообщения


def get_edit_all_data_ikb() -> InlineKeyboardMarkup:
    """Кнопки редактирования данных, добавить еще кнопки ++++"""
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Добавить группу', callback_data='add_new_groups')],
        [InlineKeyboardButton('Добавить ученика', callback_data='add_new_user')],
        [InlineKeyboardButton('Добавить время занятий', callback_data='ass_new_class_time')],
    ])
    return ikb


def get_start_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton('/edit')]
    ], resize_keyboard=True)
    return kb


def get_cancel_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton('/cancel')]
    ], resize_keyboard=True)
    return kb


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Добро пожаловать!',
                           reply_markup=get_start_kb())


@dp.message_handler(commands=['cancel'], state='*')
async def cmd_cancel(message: types.Message, state: FSMContext):
    if state is None:
        return
    await state.finish()
    await message.answer('Вы отменили действие...', reply_markup=get_start_kb())


@dp.message_handler(commands=['edit'])
async def cmd_edit_all_data(message: types.Message):
    await message.answer('Добавление данных:',
                         reply_markup=get_edit_all_data_ikb())


@dp.message_handler(commands=['1'])
async def process_command_1(message: types.Message):
    await message.reply(get_group_list(schedule=True))


@dp.callback_query_handler(lambda c: c.data == 'button1')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Нажата первая кнопка!')


@dp.message_handler(lambda message: message.text.startswith('/classtime'))
async def get_list_class_time(message: types.Message):
    """Время занятий конкретной группы"""
    group_id = int(message.text[10:])
    class_time_text = get_sql_class_time_list(group_id)
    await message.answer(class_time_text)


@dp.message_handler(commands=['2'])
async def process_command_2(message: types.Message):
    await message.reply(get_teacher_list(schedule=1))


@dp.message_handler(lambda message: message.text.startswith('/schedule'))
async def get_schedule_teachers(message: types.Message):
    """Время занятий конкретного преподавателя"""
    teacher_name = int(message.text[9:])
    schedule_teacher_text = get_schedule_teacher(teacher_name)
    await message.answer(schedule_teacher_text)


@dp.callback_query_handler(text='add_new_groups')
async def cb_add_new_groups(callback: types.CallbackQuery) -> None:
    """Добавляем новую группу"""
    await callback.message.delete()
    await callback.message.answer('Напиши название группы!',
                                  reply_markup=get_cancel_kb())
    await GroupStatesGroup.name.set()


@dp.message_handler(state=GroupStatesGroup.name)
async def handle_group_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['name'] = message.text
    await message.reply('Кол-во учеников в группе. Пример: 6')
    await GroupStatesGroup.next()


@dp.message_handler(state=GroupStatesGroup.quota)
async def handle_group_quota(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['quota'] = int(message.text)
    await message.reply('Стоимость занятия просто цифры без р. Пример: 650')
    await GroupStatesGroup.next()


@dp.message_handler(state=GroupStatesGroup.price)
async def handle_group_price(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['price'] = int(message.text)
    await message.reply('Длительность занятия просто цифра в минутах. Пример: 60')
    await GroupStatesGroup.next()


@dp.message_handler(state=GroupStatesGroup.duration)
async def handle_group_duration(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['duration'] = int(message.text)
    await message.reply('Описание. Пример: -')
    await GroupStatesGroup.next()


@dp.message_handler(state=GroupStatesGroup.description)
async def handle_group_description(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['description'] = message.text
    await message.reply('Какие школ. классы занимаются, цифры через пробел. Пример: 1, 2, 3')
    await GroupStatesGroup.next()


@dp.message_handler(state=GroupStatesGroup.grade)
async def handle_group_grade(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['grade'] = message.text
    await message.reply(f'Кто ведет эту группу введите цифру препод.\n{get_teacher_list(schedule=2)}\n Пример: 1')
    await GroupStatesGroup.next()


@dp.message_handler(state=GroupStatesGroup.teacher_id)
async def handle_group_teacher_id(message: types.Message, state: FSMContext) -> None:
    """После ответа на последний вопрос создаем группу в БД и выводим ответ"""
    async with state.proxy() as data:
        data['teacher_id'] = int(message.text)
    create_new_group(name=data['name'], quota=data['quota'],
                     price=data['price'], duration=data['duration'],
                     description=data['description'], grade=data['grade'],
                     teacher_id=data['teacher_id'])

    await message.reply('Спасибо группа создана', reply_markup=get_start_kb())
    await state.finish()


@dp.callback_query_handler(text='add_new_user')
async def cb_add_new_user(callback: types.CallbackQuery) -> None:
    """Добавляем нового ученика"""
    await callback.message.delete()
    await callback.message.answer('Напишите имя ученика!',
                                  reply_markup=get_cancel_kb())
    await UserStatesGroup.first_name.set()


@dp.message_handler(state=UserStatesGroup.first_name)
async def handle_group_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['first_name'] = message.text
    await message.reply('Напишите фамилие ученика')
    await UserStatesGroup.next()


@dp.message_handler(state=UserStatesGroup.last_name)
async def handle_group_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['last_name'] = message.text
    await message.reply('Напишите город')
    await UserStatesGroup.next()


@dp.message_handler(state=UserStatesGroup.town)
async def handle_group_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['town'] = message.text
    await message.reply('Описание, ФИО родителей, ном. тел. родителей и прочее в произвольной форме')
    await UserStatesGroup.next()


@dp.message_handler(state=UserStatesGroup.description)
async def handle_group_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['description'] = message.text
    await message.reply('День рождения в формате 25.11.1998')
    await UserStatesGroup.next()


@dp.message_handler(state=UserStatesGroup.birthday)
async def handle_group_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['birthday'] = add_date(message.text)
    await message.reply('Номер телефона в формате 8 962 412 50 81')
    await UserStatesGroup.next()


@dp.message_handler(state=UserStatesGroup.phone_number)
async def handle_group_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['phone_number'] = message.text
    await message.reply(f'Выберите группу из списка. Напишите номер группы. Пример: 2\n'
                        f'{get_group_list(schedule=False)}')
    await UserStatesGroup.next()


@dp.message_handler(state=UserStatesGroup.group_id)
async def handle_group_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['group_id'] = message.text
    create_new_user(first_name=data['first_name'], last_name=data['last_name'],
                    email=data['email'], town=data['town'],
                    description=data['description'], birthday=data['birthday'],
                    phone_number=data['phone_number'], group_id=data['group_id'])

    await message.reply('Спасибо пользователь создан', reply_markup=get_start_kb())
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp)
