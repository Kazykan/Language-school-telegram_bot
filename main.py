from dataclasses import dataclass
from tokenize import group
from typing import Type
from unicodedata import name
from sqlalchemy import  Column, create_engine, MetaData, Table, String, Integer, Text, DateTime, Boolean, ForeignKey, insert, Time, Date
from datetime import datetime, timedelta
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship
from sqlalchemy.sql import select
from typing import NamedTuple


from business import add_time

engine = create_engine('sqlite:///sqlite3.db')

session = Session(bind=engine)

Base = declarative_base()
metadata = Base.metadata


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


# t1 = Teacher(
#     first_name = 'Алия',
#     last_name = 'Кочербаева',
#     town = 'Ставрополь',
# )
# session.add(t1)
# session.commit()

# t2 = Teacher(
#     first_name = 'Евгения',
#     last_name = 'Джад',
#     town = 'Ставрополь',
# )
# session.add(t2)
# session.commit()

# g1 = Group(
#     name = 'Power Up (0-2 класс)',
#     quota = 6,
#     price = 550,
#     duration = 60,
#     grade = '0, 1, 2',
#     teacher_id = 1,
# )
# session.add(g1)
# session.commit()

# g2 = Group(
#     name = 'Go getter 1 (2-3 класс)',
#     quota = 5,
#     price = 750,
#     duration = 60,
#     grade = '2, 3',
#     teacher_id = 2,
# )
# session.add(g2)
# session.commit()

# g3 = Group(
#     name = 'Go getter 4 (6-7 класс)',
#     quota = 6,
#     price = 750,
#     duration = 60,
#     grade = '6, 7',
#     teacher_id = 1,
# )
# session.add(g3)
# session.commit()

# g4 = Group(
#     name = 'Go getter 4 (7-8 класс)',
#     quota = 6,
#     price = 750,
#     duration = 60,
#     grade = '7, 8',
#     teacher_id = 1,
# )
# session.add(g4)
# session.commit()

# u1 = User(
#     first_name = 'Ильяс',
#     last_name = 'Кочербаев',
#     town = 'Ставрополь',
#     group_id = 1,
# )
# session.add(u1)
# session.commit()

# u2 = User(
#     first_name = 'Арина',
#     last_name = 'Амбулбариева',
#     town = 'Ставрополь',
#     group_id = 2,
# )
# session.add(u2)
# session.commit()

# u3 = User(
#     first_name = 'Мелиса',
#     last_name = 'Токаева',
#     town = 'Сердара',
#     group_id = 3
# )
# session.add(u3)
# session.commit()

# u4 = User(
#     first_name = 'Иман',
#     last_name = 'Хайрулин',
#     town = 'Ставрополь',
#     group_id = 1,
# )
# session.add(u4)
# session.commit()

# u5 = User(
#     first_name = 'Динара',
#     last_name = 'Оразбаева',
#     town = 'Ставрополь',
#     group_id = 4,
# )
# session.add(u5)
# session.commit()

# u6 = User(
#     first_name = 'Мариф',
#     last_name = 'Огузов',
#     town = 'Ставрополь',
# )
# session.add(u6)
# session.commit()

# cr1 = ClassRoom(
#     name = 'Кабинет 304А - первый',
#     location = '50 лет ВКЛСМ 109',
# )
# session.add(cr1)
# session.commit

# cr2 = ClassRoom(
#     name = 'Кабинет 304А - второй',
#     location = '50 лет ВКЛСМ 109',
# )
# session.add(cr2)
# session.commit

# ct1 = ClassTime(
#     start_time = add_time(hour=9, minute=0, day=1),
#     end_time = add_time(hour=9, minute=0, day=1) + timedelta(minutes=60),
#     group_id = 1,
#     class_room_id = 1,
# )
# session.add(ct1)
# session.commit()

# ct2 = ClassTime(
#     start_time = add_time(hour=12, minute=0, day=2),
#     end_time = add_time(hour=12, minute=0, day=2) + timedelta(minutes=60),
#     group_id = 2,
#     class_room_id = 2,
# )
# session.add(ct2)
# session.commit()

# ct3 = ClassTime(
#     start_time = add_time(hour=12, minute=0, day=3),
#     end_time = add_time(hour=12, minute=0, day=3) + timedelta(minutes=60),
#     group_id = 3,
#     class_room_id = 1,
# )
# session.add(ct3)
# session.commit()

# ct4 = ClassTime(
#     start_time=add_time(hour=12, minute=0, day=5),
#     end_time=add_time(hour=12, minute=0, day=5) + timedelta(minutes=60),
#     group_id=4,
#     class_room_id=1,
# )
# session.add(ct4)
# session.commit()
#
# ct5 = ClassTime(
#     start_time=add_time(hour=15, minute=0, day=3),
#     end_time=add_time(hour=15, minute=0, day=3) + timedelta(minutes=60),
#     group_id=4,
#     class_room_id=1,
# )
# session.add(ct5)
# session.commit()


@dataclass(slots=True, frozen=True)
class GroupAdd:
    name: str
    quota: int
    price: int
    duration: int
    description: str
    grade: str
    teacher_id: int


def get_teacher_list():
    teacher_list = session.query(Teacher.last_name, Teacher.first_name, Teacher.id).all()
    text = f'Список преподавателей:'
    for teacher in teacher_list:
        text = text + f'\n{teacher[0]} {teacher[1]} расписание /schedule{teacher[2]}\n__________'
    return text


def get_schedule_teacher(teacher_id: int):
    try:
        teacher_group_tuple = session.query(
            ClassTime.class_room_id, Group.name, Teacher.first_name, ClassTime.start_time, ClassTime.end_time
        ).join(ClassTime).join(Teacher).join(ClassRoom).filter(Teacher.id == teacher_id)\
            .group_by(ClassTime.start_time).all()
    except Exception:
        return f'Ошибка ввода, преподаватель не найден'
    teacher_group_list = []
    index = 0
    for room_id in teacher_group_tuple:
        teacher_group_list.append([*room_id])
        teacher_group_list[index].append(get_classroom_name(room_id[0]))
        index += 1
    print(teacher_group_list)
    text = _get_schedule_teacher_text(teacher_group_list)
    return text


def get_classroom_name(id_classroom):
    class_room = session.query(ClassRoom.name).filter(ClassRoom.id == id_classroom).scalar()
    print(class_room)
    return class_room


def _get_schedule_teacher_text(teacher_group_list: list) -> str:
    text = f'Расписание {teacher_group_list[0][2]}\n____________\n'
    for index in teacher_group_list:
        text = text + f'{index[1]}\n' + _get_time_room_text(start_time=index[3], end_time=index[4], room=index[5])
    return text


def get_group_list():
    """Получаем список групп, распаковываем кортеж + добавляем в конец кол-во учеников в группе"""
    group_tuple = session.query(Group.id, Group.name, Group.quota, Teacher.first_name).join(Teacher).all()
    group_list = tuple_to_list_add_user_count(group_tuple=group_tuple)
    group_text = get_group_text(group_list)
    return group_text


def get_group_text(group_list: list) -> str:
    group_text = 'Список групп:\n'
    for lists in group_list:
        group_text = group_text + f'{lists[1]} - 🇺🇸 {lists[3]}\n' \
                                  f'Кол-во мест в группе: {lists[2]} - свободно мест {lists[2] - lists[4]}\n' \
                                  f'📅 Время занятий /classtime{lists[0]}\n'\
                                  f'_______________\n'
    return group_text


def get_group_grade(grade: int):
    """Получаем список групп по запросу цифры класса - grade"""
    grade_str = f'%{str(grade)}%'
    group_tuple = session.query(
        Group.id, Group.name, Group.quota, Group.price, Group.duration, Teacher.first_name)\
        .join(Teacher).filter(Group.grade.ilike(grade_str)).all()
    if group_tuple:
        group_list = tuple_to_list_add_user_count(group_tuple=group_tuple)
        return group_list
    else:
        return f'Нет групп для вашего {grade} класса'


def tuple_to_list_add_user_count(group_tuple: list) -> list:
    index = 0
    group_list = []
    for group_id in group_tuple:
        group_list.append([*group_id])
        group_list[index].append(session.query(User).filter(User.group_id == group_id[0]).count())
        index += 1
    return group_list


def get_user_free() -> list:
    """Список всех учеников которые не состоят не в каких группах"""
    user_list = session.query(
        User.id, User.first_name, User.last_name, User.birthday
    ).filter(User.group_id == None).all()
    return user_list


def create_group(name: str, quota: int, price: int, duration: int, grade: str, description: str):
    try:
        g = Group(
            name=name,
            quota=quota,
            price=price,
            duration=duration,
            grade=grade,
            description=description,
        )
        session.add(g)
        session.commit()

        group_add_now = session.query(Group.id, Group.name, Group.quota, Group.price, Group.grade, Group.description).filter(Group.name == name).get()
        return group_add_now
    except Exception:
        return f'Ошибка ввода данных'


def get_sql_class_time_list(group_id) -> str:
    """Получаем время занятий для группы"""
    class_time_list = session.query(ClassTime.id, ClassRoom.name, ClassTime.start_time, ClassTime.end_time)\
        .join(ClassRoom).filter(ClassTime.group_id == group_id).group_by(ClassTime.start_time).all()
    group_and_teacher = session.query(Group.name, Teacher.first_name).join(Group).filter(Group.id == group_id).all()[0]
    text = _get_class_time_text([*group_and_teacher], class_time_list)
    return text


def _get_class_time_text(group_and_teacher, class_time_list: list) -> str:
    text = f'{group_and_teacher[0]} - 🇺🇸 {group_and_teacher[1]}\n______время_занятий________\n'
    for class_time_tuple in class_time_list:
        class_time = [*class_time_tuple]
        text = text + _get_time_room_text(start_time=class_time[2], end_time=class_time[3], room=class_time[1])
    return text


def _get_time_room_text(start_time: datetime, end_time: datetime, room: str) -> str:
    text = f'{start_time.strftime("%A c %H:%M")} до {end_time.strftime("%H:%M")}\n{room}\n_______________\n'
    return text


print(get_schedule_teacher(1))

get_teacher_list()