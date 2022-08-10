import sqlite3

from sqlalchemy import Column, create_engine, MetaData, Table, String, Integer, Text, DateTime, Boolean,\
    ForeignKey, insert, Time, Date, or_
from datetime import datetime, timedelta
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship

"""Добавление еще одного столбца в таблицу"""
"""con = sqlite3.connect('sqlite3.db')
c = con.cursor()
c.execute("ALTER TABLE user ADD COLUMN is_active 'bool'")
con.commit()
c.close()"""


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




# t1 = Teacher(
#     first_name = 'Алия',
#     last_name = 'Кочербаева',
#     town = 'Ставрополь',
# )
# session.add(t1)
# session.commit()

# t2 = Teacher(
#     first_name = 'Евгения',
#     last_name = 'Верещагина',
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


# @dataclass(slots=True, frozen=True)
# class GroupAdd:
#     name: str
#     quota: int
#     price: int
#     duration: int
#     description: str
#     grade: str
#     teacher_id: int


def get_one_group(group_id: int) -> list:
    group_list = session.query(Group.id, Group.duration).filter(Group.id == group_id).all()[0]
    return group_list


def get_class_rooms_list():
    class_rooms_tuple = session.query(ClassRoom.id, ClassRoom.name).all()
    text = f'Список кабинетов:'
    for room in class_rooms_tuple:
        text = text + f'\n{room[0]}. {room[1]}'
    return class_rooms_tuple


def get_teacher_list(schedule):
    teacher_list = session.query(Teacher.last_name, Teacher.first_name, Teacher.id).all()
    text = f'Список преподавателей:'
    if schedule == 1:
        for teacher in teacher_list:
            text = text + f'\n{teacher[0]} {teacher[1]} расписание /schedule{teacher[2]}\n__________'
        return text
    else:
        for teacher in teacher_list:
            text = text + f'\n{teacher[2]}. {teacher[0]} {teacher[1]}'
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
    text = _get_schedule_teacher_text(teacher_group_list)
    return text


def get_classroom_name(id_classroom):
    class_room = session.query(ClassRoom.name).filter(ClassRoom.id == id_classroom).scalar()
    return class_room


def _get_schedule_teacher_text(teacher_group_list: list) -> str:
    text = f'Расписание {teacher_group_list[0][2]}\n____________\n'
    for index in teacher_group_list:
        text = text + f'{index[1]}\n' + _get_time_room_text(start_time=index[3], end_time=index[4], room=index[5])
    return text


def get_groups_list(schedule: bool) -> str:
    """Получаем список групп, распаковываем кортеж + добавляем в конец кол-во учеников в группе"""
    group_tuple = session.query(Group.id, Group.name, Group.quota, Teacher.first_name).join(Teacher).all()
    group_list = tuple_to_list_add_user_count(group_tuple=group_tuple)
    group_text = get_group_text(group_list, schedule)
    return group_text


def get_group_text(group_list: list, schedule: bool) -> str:
    group_text = 'Список групп:\n'
    for lists in group_list:
        if not schedule:
            group_text = group_text + f'{lists[0]}. '
        group_text = group_text + f'{lists[1]} - 🇺🇸 {lists[3]}\n'
        if schedule:
            group_text = group_text + f'Кол-во мест в группе: {lists[2]} - свободно мест {lists[2] - lists[4]}\n'\
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
        group_list[index].append(session.query(User.id).filter(User.group_id == group_id[0]).count())
        index += 1
    return group_list


def get_user_free() -> list:
    """Список всех учеников которые не состоят не в каких группах"""
    user_list = session.query(
        User.id, User.first_name, User.last_name, User.birthday
    ).filter(User.group_id == None).all()
    return user_list


def get_sql_class_time_list(group_id, edit: bool) -> str:
    """Получаем время занятий для группы"""
    class_time_list = session.query(ClassTime.id, ClassRoom.name, ClassTime.start_time, ClassTime.end_time)\
        .join(ClassRoom).filter(ClassTime.group_id == group_id).group_by(ClassTime.start_time).all()
    if class_time_list:
        group_and_teacher = session.query(Group.name, Teacher.first_name).join(Group).filter(Group.id == group_id).all()[0]
        text = _get_class_time_text([*group_and_teacher], class_time_list, edit)
        return text
    else:
        return f'Нет расписания'


def _get_class_time_text(group_and_teacher, class_time_list: list, edit: bool) -> str:
    text = f'{group_and_teacher[0]} - 🇺🇸 {group_and_teacher[1]}\n______время_занятий________\n'
    for class_time_tuple in class_time_list:
        class_time = [*class_time_tuple]
        text = text + _get_time_room_text(start_time=class_time[2], end_time=class_time[3], room=class_time[1])
        if edit:
            text = text + f'удалить - /del_ct#{class_time[0]} \n_______________\n'
    return text


def _get_time_room_text(start_time: datetime, end_time: datetime, room: str) -> str:
    text = f'{start_time.strftime("%A c %H:%M")} до {end_time.strftime("%H:%M")}\n{room}\n'
    return text


def create_new_group(name: str, quota: int, price: int, duration: int, description: str, grade: str, teacher_id: int):
    try:
        groups = Group(
            name=str(name),
            quota=int(quota),
            price=int(price),
            duration=int(duration),
            description=str(description),
            grade=str(grade),
            teacher_id=int(teacher_id),
        )
        session.add(groups)
        session.commit()
        return f'Группа создана'
    except ValueError as e:
        return f'{create_new_group.__qualname__} ошибка ввода данных'


def create_new_user(first_name: str, last_name: str, description: str, phone_number: str, is_active: bool,
                    email: str = None, town: str = None, birthday: str = None, group_id: int = None):
    try:
        users = User(
            first_name=str(first_name),
            last_name=str(last_name),
            email=str(email),
            town=str(town),
            description=str(description),
            birthday=birthday,
            phone_number=str(phone_number),
            is_active=bool(is_active),
            group_id=int(group_id),
        )
        session.add(users)
        session.commit()
    except ValueError as e:
        return f'{create_new_user.__qualname__} ошибка ввода данных'


def check_class_time_busy(start_time: datetime, end_time: datetime, class_room_id: int, group_id: int) -> list:
    """Проверка занят кабинет на это время и если занять то какими группами"""
    time_busy_at_cr = session.query(ClassTime.id, ClassTime.class_room_id, ClassTime.start_time, ClassTime.end_time)\
        .filter(or_(ClassTime.start_time.between(start_time, end_time),
                ClassTime.end_time.between(start_time, end_time)),
                ClassTime.class_room_id == class_room_id).order_by(ClassTime.start_time).all()
    check_list = []
    teacher_id = int(session.query(Group.teacher_id).filter(Group.id == group_id).scalar())
    time_busy_at_teacher = session.query(
        ClassTime.id, ClassTime.class_room_id, Group.id, ClassTime.start_time, ClassTime.end_time)\
        .join(Group).filter(or_(ClassTime.start_time.between(start_time, end_time),
                                ClassTime.end_time.between(start_time, end_time)),
                            Group.teacher_id == teacher_id).order_by(ClassTime.start_time).all()
    if time_busy_at_cr or time_busy_at_teacher:
        check_list.extend([False, time_busy_at_cr, time_busy_at_teacher])
        return check_list
    else:
        text = create_new_class_time(start_time=start_time, end_time=end_time,
                                     class_room_id=class_room_id, group_id=group_id)
        check_list.extend([True, text])
        return check_list


def create_new_class_time(start_time: datetime, end_time: datetime, class_room_id: int, group_id: int) -> str:
    try:
        class_time_add = ClassTime(
            start_time=start_time,
            end_time=end_time,
            group_id=int(group_id),
            class_room_id=int(class_room_id),
        )
        session.add(class_time_add)
        session.commit()
        return f'Время занятий добавлено'
    except ValueError as e:
        return f'{create_new_class_time.__qualname__} ошибка ввода данных'

start_times = datetime(year=2021, month=11, day=1, hour=11, minute=10)
end_times = datetime(year=2021, month=11, day=7, hour=12, minute=45)
print(check_class_time_busy(start_time=start_times, end_time=end_times, class_room_id=1, group_id=1))
# print(session.query(ClassTime.id, ClassTime.class_room_id, ClassTime.start_time, ClassTime.end_time).filter(or_(
#     ClassTime.start_time.between(start_times, end_time),
#     ClassTime.end_time.between(start_times, end_time)),
#     ClassTime.class_room_id == 1).order_by(ClassTime.start_time).all())
# print(session.query(Group.teacher_id, Teacher.first_name).join(Teacher).filter(Group.id == 1).all())
# print(get_schedule_teacher(1))
# get_teacher_list(schedule=2)
# print(get_group_list(schedule=True))
# print(session.query(User.group_id, User.first_name, User.last_name, User.is_active).all())
# print(session.query(User.id).filter(User.group_id == 1).count())
# print(get_sql_class_time_list(group_id=4, edit=True))
# print(session.query(Group.id, Group.name, Group.teacher_id, Group.grade).filter(Group.id == 5).all())
# print(create_new_group(name='dfsdf', quota='fdsfsdf', price='fdsfs', duration=564, description='fsdfs', grade='fsdfs', teacher_id=1))

# print(session.query(ClassRoom.id, ClassRoom.name, ClassRoom.location).all())
# print(session.query(Group.id, Group.duration).filter(Group.id == 2).all()[0])
# i = session.query(Group).filter(Group.id == 6).delete()
# session.commit()
#
# print(session.query(Group.id, Group.name, Group.quota, Group.price, Group.duration).all())
