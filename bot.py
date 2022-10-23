"""Бот Языковой студии, возможность добавления ученик, групп, классов, времени занятий"""

from datetime import timedelta
from email import message
import logging
import re

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton,\
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from business import get_groups_list, get_class_time, get_teacher_list, \
    create_new_group, create_new_user, get_class_rooms_list, get_one_group, check_class_time_busy, \
    add_date, add_time, get_schedule_teacher, get_groups_reservation_text
from stategroup import GradeSearchStatesGroup, GroupStatesGroup, UserStatesGroup, \
    ClassTimeStatesGroup

from config import TELEGRAM_TOKEN, ADMIN_ID, CHANNEL_ID


bot = Bot(token=TELEGRAM_TOKEN)  # Объект бота
dp = Dispatcher(bot,
                storage=MemoryStorage())  # Диспетчер для бота
logging.basicConfig(level=logging.INFO)  # Вкл логирование, чтобы не пропустить важные сообщения


acl = (172457394,)
# def admin_only_f(message):
#     if message.from_user.id not in acl:
#         return True
#     else:
#         print(message.from_user.id)
admin_only = lambda message: message.from_user.id in ADMIN_ID


async def send_message_chanel(text: str):
    """Отправка сообщения в канал"""
    await bot.send_message(CHANNEL_ID, text)


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    """Запуск начайльной кнопки"""
    await bot.send_message(chat_id=message.from_user.id,
                           text='Добро пожаловать!',
                           reply_markup=get_start_ikb())


def get_start_ikb() -> InlineKeyboardMarkup:
    """Кнопки первые: Записаться, ученику, учителю"""
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Записаться в группу 🇬🇧', callback_data='reservation')],
        [InlineKeyboardButton('Ученику расписание 🗓', callback_data='user_schedule')],
        [InlineKeyboardButton('Учителю 👨‍🏫', callback_data='edit')],
    ], reply_markup=ReplyKeyboardRemove())
    return ikb


def get_start_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton('/edit')],
        [KeyboardButton('/start')],
        [KeyboardButton('/back')],
    ], resize_keyboard=True)
    return kb


def get_cancel_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton('/cancel')]
    ], resize_keyboard=True)
    return kb


@dp.callback_query_handler(admin_only, text='edit')
async def cb_teacher_keyboard(callback: types.CallbackQuery) -> None:
    """Отработка кнопки учителю"""
    await callback.message.delete()
    await callback.message.answer('Добавление данных:',
                                  reply_markup=get_edit_all_data_ikb())



def get_edit_all_data_ikb() -> InlineKeyboardMarkup:
    """Кнопки редактирования данных, добавить еще кнопки ++++"""
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Доб.|удалить|поправить группу', callback_data='tasks_group')],
        [InlineKeyboardButton('Доб.|удалить|поправить ученика', callback_data='tasks_user')],
        [InlineKeyboardButton('Доб.|удалить время занятий', callback_data='tasks_class_time')],
        [InlineKeyboardButton('Расписания учителей', callback_data='teacher_schedule')],
    ], reply_markup=ReplyKeyboardRemove())
    return ikb


@dp.callback_query_handler(admin_only, text='tasks_group')
async def cb_tasks_group(callback: types.CallbackQuery) -> None:
    """Отработка кнопки Добавить|удалить|поправить группу"""
    await callback.message.delete()
    await callback.message.answer('Добавление данных:',
                                  reply_markup=get_tasks_group_ikb())



def get_tasks_group_ikb() -> InlineKeyboardMarkup:
    """Кнопки редактирования группы, Добавить|удалить|поправить группу"""
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Добавить группу', callback_data='add_new_group')],
        [InlineKeyboardButton('Удалить группу', callback_data='remove_group')],
        [InlineKeyboardButton('Поправить данные группы', callback_data='fix_group')],
        [InlineKeyboardButton('Назад', callback_data='edit')],
    ], reply_markup=ReplyKeyboardRemove())
    return ikb


@dp.callback_query_handler(admin_only, text='tasks_user')
async def cb_tasks_groups(callback: types.CallbackQuery) -> None:
    """Отработка кнопки Добавить|удалить|поправить ученика"""
    await callback.message.delete()
    await callback.message.answer('Добавление данных:',
                                  reply_markup=get_tasks_user_ikb())



def get_tasks_user_ikb() -> InlineKeyboardMarkup:
    """Кнопки редактирования ученика, Добавить|удалить|поправить ученика"""
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Добавить ученика', callback_data='add_new_user')],
        [InlineKeyboardButton('Удалить ученика', callback_data='remove_user')],
        [InlineKeyboardButton('Поправить данные ученика', callback_data='fix_user')],
        [InlineKeyboardButton('Назад', callback_data='edit')],
    ], reply_markup=ReplyKeyboardRemove())
    return ikb


@dp.callback_query_handler(admin_only, text='tasks_class_time')
async def cb_tasks_class_time(callback: types.CallbackQuery) -> None:
    """Отработка кнопки Добавить|удалить время занятий"""
    await callback.message.delete()
    await callback.message.answer('Добавление данных:',
                                  reply_markup=get_tasks_class_time_ikb())



def get_tasks_class_time_ikb() -> InlineKeyboardMarkup:
    """Кнопки редактирования ученика, Добавить|удалить|поправить ученика"""
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Добавить время занятий', callback_data='add_class_time')],
        [InlineKeyboardButton('Удалить время занятий', callback_data='remove_class_time')],
        [InlineKeyboardButton('Назад', callback_data='edit')],
    ], reply_markup=ReplyKeyboardRemove())
    return ikb


@dp.message_handler(commands=['cancel'], state='*')
async def cmd_cancel(message: types.Message, state: FSMContext):
    if state is None:
        return
    await state.finish()
    await message.answer('Вы отменили действие...', reply_markup=get_start_ikb())


@dp.callback_query_handler(text='user_schedule')
async def cb_group_schedule(callback: types.CallbackQuery) -> None:
    """Расписание для группы"""
    await callback.message.delete()
    await callback.message.answer(get_groups_list(schedule=True))


@dp.message_handler(lambda message: message.text.startswith('/classtime'))
async def get_list_class_time(message: types.Message):
    """Время занятий конкретной группы"""
    group_id = int(message.text[10:])
    class_time_text = get_class_time(group_id, is_edit=False)
    await message.answer(class_time_text)


@dp.callback_query_handler(text='teacher_schedule')
async def cb_teacher_schedule(callback: types.CallbackQuery) -> None:
    """Расписание для учителя"""
    await callback.message.delete()
    await callback.message.answer(get_teacher_list(schedule=1))


@dp.message_handler(lambda message: message.text.startswith('/schedule'))
async def get_schedule_teachers(message: types.Message):
    """Время занятий конкретного преподавателя"""
    teacher_name = int(message.text[9:])
    schedule_teacher_text = get_schedule_teacher(teacher_name)
    await message.answer(schedule_teacher_text)


@dp.callback_query_handler(text='add_new_group')
async def cb_add_new_group(callback: types.CallbackQuery) -> None:
    """Добавляем новую группу"""
    await callback.message.delete()
    await callback.message.answer('Напиши название группы!',
                                  reply_markup=get_cancel_kb())
    await GroupStatesGroup.name.set()


@dp.message_handler(state=GroupStatesGroup.name)
async def handle_group_name(message: types.Message, state: FSMContext) -> None:
    """Добавляем новую группу - 2 пункт"""
    async with state.proxy() as data:
        data['name'] = message.text
    await message.reply('Кол-во учеников в группе. Пример: 6')
    await GroupStatesGroup.next()


@dp.message_handler(state=GroupStatesGroup.quota)
async def handle_group_quota(message: types.Message, state: FSMContext) -> None:
    """Добавляем новую группу - 3 пункт"""
    async with state.proxy() as data:
        data['quota'] = int(message.text)
    await message.reply('Стоимость занятия просто цифры без р. Пример: 650')
    await GroupStatesGroup.next()


@dp.message_handler(state=GroupStatesGroup.price)
async def handle_group_price(message: types.Message, state: FSMContext) -> None:
    """Добавляем новую группу - 4 пункт"""
    async with state.proxy() as data:
        data['price'] = int(message.text)
    await message.reply('Длительность занятия просто цифра в минутах. Пример: 60')
    await GroupStatesGroup.next()


@dp.message_handler(state=GroupStatesGroup.duration)
async def handle_group_duration(message: types.Message, state: FSMContext) -> None:
    """Добавляем новую группу - 5 пункт"""
    async with state.proxy() as data:
        data['duration'] = int(message.text)
    await message.reply('Описание. Пример: -')
    await GroupStatesGroup.next()


@dp.message_handler(state=GroupStatesGroup.description)
async def handle_group_description(message: types.Message, state: FSMContext) -> None:
    """Добавляем новую группу - 6 пункт"""
    async with state.proxy() as data:
        data['description'] = message.text
    await message.reply('Какие школ. классы занимаются, цифры через пробел. Пример: 1 2 3')
    await GroupStatesGroup.next()


@dp.message_handler(state=GroupStatesGroup.grade)
async def handle_group_grade(message: types.Message, state: FSMContext) -> None:
    """Добавляем новую группу - 7 пункт"""
    try:
        async with state.proxy() as data:
            data['grade'] = [int(i) for i in message.text.split()]  # Разделяем и преобразуем в цифры
        await message.reply(f'Кто ведет эту группу введите цифру препод.\n{get_teacher_list(schedule=2)}\n Пример: 1')
        await GroupStatesGroup.next()
    except ValueError:
        await message.reply('Не верно введены данные\n'
        'Какие школ. классы занимаются, цифры через пробел. Пример: 1 2 3')


@dp.message_handler(state=GroupStatesGroup.teacher_id)
async def handle_group_teacher_id(message: types.Message, state: FSMContext) -> None:
    """После ответа на последний вопрос создаем группу в БД и выводим ответ"""
    async with state.proxy() as data:
        data['teacher_id'] = int(message.text)
    create_new_group(name=data['name'], quota=data['quota'],
                     price=data['price'], duration=data['duration'],
                     description=data['description'], grades=data['grade'],
                     teacher_id=data['teacher_id'])

    await message.reply('Спасибо группа создана', reply_markup=get_start_kb())
    await state.finish()


@dp.callback_query_handler(text='reservation')
async def cb_search_group_by_grade(callback: types.CallbackQuery) -> None:
    """Поиск групп по классам для записи на тестирование"""
    await callback.message.delete()
    await callback.message.answer('Напишите класс в котором учитесь вы или ваш ребенок, 0 - дошкольник, 12 - студент, 13 - взрослый',
                                  reply_markup=get_cancel_kb())
    await GradeSearchStatesGroup.grade_name.set()


@dp.message_handler(state=GradeSearchStatesGroup.grade_name)
async def cb_search_group_by_grade_grade_name(message: types.Message, state: FSMContext) -> None:
    """Поиск групп по классам для записи на тестирование"""
    async with state.proxy() as data:
        data['grade_name'] = int(message.text)
    group_list = get_groups_reservation_text(grade_number=data['grade_name'])
    await message.reply(f'Напишите номер группы который вам подходит по рассписанию: \n{group_list}')
    await GradeSearchStatesGroup.group_id.set()



@dp.message_handler(state=GradeSearchStatesGroup.group_id)
async def cb_search_group_by_grade_group_id(message: types.Message, state: FSMContext) -> None:
    """Поиск групп по классам для записи на тестирование"""
    async with state.proxy() as data:
        data['group_id'] = (message.text)
    await message.reply('Напишите номер телефона для связи и ваше имя:\n')
    await GradeSearchStatesGroup.contact_info.set()


@dp.message_handler(state=GradeSearchStatesGroup.contact_info)
async def cb_search_group_by_grade_contact_info(message: types.Message, state: FSMContext) -> None:
    """Поиск групп по классам для записи на тестирование"""
    async with state.proxy() as data:
        data['contact_info'] = (message.text)
    await message.reply('Большое спасибо, мы обязятельно с вами свяжемся')
    text_reservation = get_groups_reservation_text(grade_number=data['grade_name'])
    text_reservation += f"\n\ncontact - {data['contact_info']}\n group: {data['group_id']}. grade - {data['grade_name']}"
    await send_message_chanel(text_reservation)
    await state.finish()


@dp.callback_query_handler(text='add_new_user')
async def cb_add_new_user(callback: types.CallbackQuery) -> None:
    """Добавляем нового ученика"""
    await callback.message.delete()
    await callback.message.answer('Напишите имя ученика!',
                                  reply_markup=get_cancel_kb())
    await UserStatesGroup.first_name.set()


@dp.message_handler(state=UserStatesGroup.first_name)
async def cb_add_new_user_first_name(message: types.Message, state: FSMContext) -> None:
    """Добавляем нового ученика"""
    async with state.proxy() as data:
        data['first_name'] = message.text
    await message.reply('Напишите фамилие ученика')
    await UserStatesGroup.next()


@dp.message_handler(state=UserStatesGroup.last_name)
async def cb_add_new_user_last_name(message: types.Message, state: FSMContext) -> None:
    """Добавляем нового ученика"""
    async with state.proxy() as data:
        data['last_name'] = message.text
    await message.reply('Напишите город')
    await UserStatesGroup.next()


@dp.message_handler(state=UserStatesGroup.town)
async def cb_add_new_user_town(message: types.Message, state: FSMContext) -> None:
    """Добавляем нового ученика"""
    async with state.proxy() as data:
        data['town'] = message.text
    await message.reply('Описание, ФИО родителей, ном. тел. родителей и прочее в произвольной форме')
    await UserStatesGroup.next()


@dp.message_handler(state=UserStatesGroup.description)
async def cb_add_new_user_description(message: types.Message, state: FSMContext) -> None:
    """Добавляем нового ученика"""
    async with state.proxy() as data:
        data['description'] = message.text
    await message.reply('День рождения в формате 25.11.1998')
    await UserStatesGroup.next()


@dp.message_handler(state=UserStatesGroup.birthday)
async def cb_add_new_user_birthday(message: types.Message, state: FSMContext) -> None:
    """Добавляем нового ученика"""
    async with state.proxy() as data:
        data['birthday'] = add_date(message.text)
    await message.reply('Номер телефона в формате 8 962 412 50 81')
    await UserStatesGroup.next()


@dp.message_handler(state=UserStatesGroup.phone_number)
async def cb_add_new_user_phone_number(message: types.Message, state: FSMContext) -> None:
    """Добавляем нового ученика"""
    async with state.proxy() as data:
        data['phone_number'] = message.text
    await message.reply(f'Выберите группу из списка. Напишите номер группы. Пример: 2\n'
                        f'{get_groups_list(schedule=False)}')
    await UserStatesGroup.next()


@dp.message_handler(state=UserStatesGroup.group_id)
async def cb_add_new_user_group_id(message: types.Message, state: FSMContext) -> None:
    """Добавляем нового ученика - запускаем проверку и добавляем ученика"""
    async with state.proxy() as data:
        data['group_id'] = message.text
    create_new_user(first_name=data['first_name'], last_name=data['last_name'],
                    town=data['town'], description=data['description'], birthday=data['birthday'],
                    phone_number=data['phone_number'], group_id=data['group_id'], is_active=True)

    await message.reply('Спасибо пользователь создан', reply_markup=get_start_kb())
    await state.finish()


@dp.callback_query_handler(text='add_class_time')
async def cb_add_classtime(callback: types.CallbackQuery) -> None:
    """Добавляем время занятий для группы"""
    await callback.message.delete()
    await callback.message.answer(f'Введите номер группы просто цифру. Пример: 5\n{get_groups_list(schedule=False)}',
                                  reply_markup=get_cancel_kb())
    await ClassTimeStatesGroup.group_id.set()


@dp.message_handler(state=ClassTimeStatesGroup.group_id)
async def cb_add_classtime_group_id(message: types.Message, state: FSMContext) -> None:
    """Добавляем время занятий для группы"""
    async with state.proxy() as data:
        data['group_id'] = int(message.text)

    await message.reply(f'{get_class_time(data["group_id"], is_edit=True)} Введите номер кабинета. Пример 1\n'
                        f'{get_class_rooms_list()}')
    await ClassTimeStatesGroup.next()


@dp.message_handler(state=ClassTimeStatesGroup.class_room_id)
async def cb_add_classtime_class_room_id(message: types.Message, state: FSMContext) -> None:
    """Добавляем время занятий для группы"""
    async with state.proxy() as data:
        data['class_room_id'] = int(message.text)

    await message.reply('Введите время начала занятий в формате день недели цифрой 1-пн, 2-вт, 3-ср, далее 09-00.\n'
                        'Пример: 5 17-30\n')
    await ClassTimeStatesGroup.next()


@dp.message_handler(state=ClassTimeStatesGroup.start_time)
async def cb_add_classtime_start_time(message: types.Message, state: FSMContext) -> None:
    """Добавляем время занятий для группы - проверка занято ли это время в кабинете и личное время преподавателя"""
    try:
        async with state.proxy() as data:
            times = re.split(' |-', message.text)
            data['start_time'] = add_time(day=int(times[0]), hour=int(times[1]), minute=int(times[2]))
            duration = get_one_group(group_id=data['group_id'])[1]
            data['end_time'] = data['start_time'] + timedelta(minutes=duration)
    except ValueError:
        await message.reply('Не верно введены данные')
    check_class_time_list = check_class_time_busy(start_time=data['start_time'], end_time=data['end_time'],
                                                  class_room_id=data['class_room_id'], group_id=data['group_id'])
    if check_class_time_list[0]:
        await message.reply(check_class_time_list[1])
        await state.finish()
    else:
        await message.reply(check_class_time_list[1])


if __name__ == "__main__":
    executor.start_polling(dp)
