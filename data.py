from email.policy import default
from sqlalchemy import  Column, create_engine, MetaData, Table, String, Integer, Text, DateTime, Boolean, ForeignKey
from datetime import datetime

metadata = MetaData()

class Teacher(Base):
    __tablename__ = 'teacher'
    id = Column(Integer(), primary_key=True)
    first_name = Column(String(15), nullable=False)
    last_name = Column(String(20), nullable=False)
    email = Column(String(50))
    town = Column(String(40))
    description = Column(Text())
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

class Group(Base):
    """Группы с максимальным кол-вом учеников, ценой и длительностью занятия"""
    __tablename__ = 'group'
    id = Column(Integer(), primary_key=True)
    name = Column(String(100), nullable=False)
    quota = Column(Integer(),  nullable=False)
    price = Column(Integer(),  nullable=False)
    duration = Column(Integer(),  nullable=False)
    description = Column(Text())
    grade = Column(String(10), nullable=False)

    teacher_id = Column(Integer(), ForeignKey("teacher.id"))
    teacher = relationship('Teacher', backref="group")

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(15), nullable=False)
    last_name = Column(String(20), nullable=False)
    email = Column(String(50))
    town = Column(String(40))
    description = Column(Text())
    birthday = Column(Date())
    phone_number = Column(String(12))
    is_active = Column(Boolean, default=True)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    group_id = Column(Integer(), ForeignKey("group.id"))
    group = relationship('Group', backref="user")

class ClassRoom(Base):
    __tablename__ = 'class_room'
    id = Column(Integer(), primary_key=True)
    name = Column(String(100), nullable=False)
    location = Column(String(20),  nullable=False)
    description = Column(Text())


class ClassTime(Base):
    __tablename__ = 'class_time'
    id = Column(Integer(), primary_key=True)
    start_time = Column(DateTime(), nullable=False)
    end_time = Column(DateTime(), nullable=False)

    group_id = Column(Integer(), ForeignKey("group.id"))
    group = relationship('Group', backref="class_time")
    class_room_id = Column(Integer(), ForeignKey('class_room.id'))
    class_room = relationship('ClassRoom', backref="class_time")


Base.metadata.create_all(engine)


button_hi = KeyboardButton('Привет 👋')

greet_kb = ReplyKeyboardMarkup()
greet_kb.add(button_hi)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply('Привет!', reply_markup=greet_kb)


greet_kb1 = ReplyKeyboardMarkup(resize_keyboard=True).add(button_hi)


@dp.message_handler(commands=['hi1'])
async def process_hi1_command(message: types.Message):
    await message.reply('Первое - изменяем размер клавиатуры', reply_markup=greet_kb1)


greet_kb2 = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
).add(button_hi)


@dp.message_handler(commands=['hi2'])
async def process_hi2_command(message: types.Message):
    await message.reply("Второе - прячем клавиатуру после одного нажатия", reply_markup=greet_kb2)


button1 = KeyboardButton('1️⃣')
button2 = KeyboardButton('2️⃣')
button3 = KeyboardButton('3️⃣')

markup3 = ReplyKeyboardMarkup().add(
    button1).add(button2).add(button3)  # расставляет кнопки одну под одной

markup4 = ReplyKeyboardMarkup().row(
    button1, button2, button3
)

markup5 = ReplyKeyboardMarkup().row(
    button1, button2, button3
).add(KeyboardButton('Средний ряд'))

button4 = KeyboardButton('4️⃣')
button5 = KeyboardButton('5️⃣')
button6 = KeyboardButton('6️⃣')
markup5.row(button4, button5)
markup5.insert(button6)


@dp.message_handler(commands=['hi3'])
async def process_hi3_command(message: types.Message):
    await message.reply("Третье - добавляем больше кнопок", reply_markup=markup3)


@dp.message_handler(commands=['hi4'])
async def process_hi4_command(message: types.Message):
    await message.reply("Четвертое - расставляем кнопки в ряд", reply_markup=markup4)


@dp.message_handler(commands=['hi5'])
async def process_hi5_command(message: types.Message):
    await message.reply("Пятое - добавляем ряды кнопок", reply_markup=markup5)

inline_btm_1 = InlineKeyboardButton("Первая кнопка!", callback_data='button1')
inline_kb1 = InlineKeyboardMarkup().add(inline_btm_1)