from dataclasses import dataclass
from datetime import datetime, date, timedelta
import locale
from sqlalchemy import create_engine, or_, select, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from main import Teacher, Grade, Group, ClassRoom, ClassTime, User, group_mtm_grade

engine = create_engine('sqlite:///sqlite3.db')

session = Session(bind=engine)
Base = declarative_base()
metadata = Base.metadata


locale.setlocale(locale.LC_ALL, ('ru_RU', 'UTF-8'))


def add_time(hour: int, minute: int, day: int) -> dataclass:
    times = datetime(year=2021, month=11, day=day, hour=hour, minute=minute)
    return times


def add_date(dates: str) -> date:
    temp = dates.split('.')
    edit_date = date(year=int(temp[2]), month=int(temp[1]), day=int(temp[0]))
    return edit_date


def get_one_group(group_id: int) -> list:
    group_list = session.query(Group.id, Group.duration).filter(Group.id == group_id).all()[0]
    return group_list


def get_class_rooms_list():
    class_rooms_tuple = session.query(ClassRoom.id, ClassRoom.name).all()
    text = 'Список кабинетов:'
    for room in class_rooms_tuple:
        text = text + f'\n{room[0]}. {room[1]}'
    return class_rooms_tuple


def get_teacher_list(schedule):
    teacher_list = session.query(Teacher.last_name, Teacher.first_name, Teacher.id).all()
    text = 'Список преподавателей:'
    if schedule == 1:
        for teacher in teacher_list:
            text = text + f'\n{teacher[0]} {teacher[1]} расписание /schedule{teacher[2]}\n__________'
        return text
    else:
        for teacher in teacher_list:
            text = text + f'\n{teacher[2]}. {teacher[0]} {teacher[1]}'
        return text


def get_schedule_teacher(teacher_id: int):
    """Получить расписание учителя"""
    try:
        teacher_group_tuple = session.query(
            ClassTime.class_room_id, Group.id, Teacher.first_name, ClassTime.start_time, ClassTime.end_time
        ).join(ClassTime).join(Teacher).join(ClassRoom).filter(Teacher.id == teacher_id)\
            .group_by(ClassTime.start_time).all()
    except ValueError:
        return 'Ошибка ввода, преподаватель не найден'
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
    text = f'-- Расписание {teacher_group_list[0][2]} --\n'
    for index in teacher_group_list:
        text = text + f'{"-"*22}\n{get_group_name(index[1])}\n' + _get_time_room_text(start_time=index[3], end_time=index[4], room=index[5])
    return text


def get_group_name(group_id) -> str:
    """Получаем название группы + классы которые там учаться"""
    group_name = session.query(Group).filter_by(id=group_id).first()
    return group_name


def _get_time_room_text(start_time: datetime, end_time: datetime, room: str) -> str:
    text = f'{start_time.strftime("%a c %H:%M")} до {end_time.strftime("%H:%M")}\n{room}\n'
    return text


def get_groups_list(schedule: bool) -> str:
    """Получаем список групп, добавляем в конец кол-во учеников в группе"""
    groups = session.query(Group).join(Teacher).all()
    group_text = 'Список групп:\n'
    for group in groups:
        if not schedule:
            group_text += f'{group.id}. '
        group_text += f'{group} - 🇺🇸 {group.teacher.first_name}\n'
        if schedule:
            group_text += f'{is_place_group(group_id=group.id)}\n'\
                          f'📅 Время занятий /classtime{group.id}\n{"-"*15}\n'
    return group_text


def is_place_group(group_id: int) -> str:
    """Есть место в группе текстом"""
    count_user = get_count_user_in_group(group_id=group_id)
    quota = session.query(Group.quota).filter(Group.id == group_id).scalar()
    if count_user <= quota:
        text_place = '✅ есть свободные места'
    else:
        text_place = '❌ нет мест'
    return text_place


def get_count_user_in_group(group_id: int) -> int:
    """Получаем кол-во учеников в группе"""
    count_user = session.query(User.id).filter(User.group_id == group_id).count()
    return count_user


def get_user_free() -> list:
    """Список всех учеников которые не состоят не в каких группах"""
    users_free = session.query(
        User.id, User.first_name, User.last_name, User.birthday
    ).filter(User.group_id == None).all()
    return users_free


# def get_class_time(group_id, is_edit: bool) -> str:
#     """Получаем время занятий для группы"""
#     class_time_list = session.query(ClassTime.id, ClassRoom.name, ClassTime.start_time, ClassTime.end_time)\
#         .join(ClassRoom).filter(ClassTime.group_id == group_id).group_by(ClassTime.start_time).all()
#     if class_time_list:
#         group_and_teacher = session.query(Group.name, Teacher.first_name).join(Group).filter(Group.id == group_id).all()[0]
#         text = _get_class_time_text([*group_and_teacher], class_time_list, edit)
#         return text
#     else:
#         return 'Нет расписания'


def get_class_time(group_id, is_edit: bool) -> str:
    """Получаем время занятий для группы"""
    class_times = session.query(ClassTime).filter(ClassTime.group_id == group_id).\
        join(Group, Group.id==ClassTime.group_id).\
        join(ClassRoom, ClassRoom.id==ClassTime.class_room_id).all()
    if class_times:
        teacher_full_name = get_teacher_full_name(teacher_id=class_times[0].group.teacher_id)
        text = f'{class_times[0].group}\n🧑‍🏫 {teacher_full_name}\n----- время занятий ------\n\n'
        for one in class_times:
            text += _get_time_room_text(start_time=one.start_time,
                                        end_time=one.end_time,
                                        room=one.class_room.name)
            if is_edit:
                text += f'🇽 удалить - /del_ct_{one.id}\n'
            text += f' {"- " * 20}\n'
        return text
    else:
        return '❌ Нет расписания'


def get_teacher_full_name(teacher_id: int) -> str:
    """Получаем фамилие и имя преподователя"""
    full_name = session.query(Teacher).filter(Teacher.id == teacher_id).first()
    full_name_text = f'{full_name}'
    return full_name_text


def create_new_group(name: str, quota: int, price: int, duration: int, description: str, grades: list, teacher_id: int):
    """Создание группы и создание связей со школьными классами которые там учаться"""
    try:
        group = Group(
            name=str(name),
            quota=int(quota),
            price=int(price),
            duration=int(duration),
            description=str(description),
            teacher_id=int(teacher_id),
        )
        session.add(group)
        session.commit()

        add_relation_group_grade(group_id=group.id, list_grades=grades)
        return 'Группа создана'
    except ValueError:
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
    except ValueError:
        return f'{create_new_user.__qualname__} ошибка ввода данных'


def check_class_time_busy(start_time: datetime, end_time: datetime, class_room_id: int, group_id: int) -> list:
    """Проверка занят кабинет на это время и если занять то какими группами.
    Прибавляем 1 минуту с начала занятий и отнимаем 1 минуту с конца занятий, т.к. занятия могут идти вплотную"""
    start_time_add_1m = start_time + timedelta(minutes=1)
    end_time_minus_1m = end_time - timedelta(minutes=1)
    time_busy_at_cr = session.query(ClassTime.id, ClassTime.class_room_id, ClassTime.start_time, ClassTime.end_time)\
        .filter(or_(ClassTime.start_time.between(start_time_add_1m, end_time_minus_1m),
                ClassTime.end_time.between(start_time_add_1m, end_time_minus_1m)),
                ClassTime.class_room_id == class_room_id).order_by(ClassTime.start_time).all()
    check_list = []
    teacher_id = int(session.query(Group.teacher_id).filter(Group.id == group_id).scalar())
    time_busy_at_teacher = session.query(
        ClassTime.id, ClassTime.class_room_id, Group.id, ClassTime.start_time, ClassTime.end_time)\
        .join(Group).filter(or_(ClassTime.start_time.between(start_time_add_1m, end_time_minus_1m),
                                ClassTime.end_time.between(start_time_add_1m, end_time_minus_1m)),
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
    """Добавляем время занятий в БД"""
    try:
        class_time_add = ClassTime(
            start_time=start_time,
            end_time=end_time,
            group_id=int(group_id),
            class_room_id=int(class_room_id),
        )
        session.add(class_time_add)
        session.commit()
        return 'Время занятий добавлено'
    except ValueError:
        return f'{create_new_class_time.__qualname__} ошибка ввода данных'


def add_relation_group_grade(group_id: str, list_grades: list) -> None:
    """Добавление в группу списком классы которыe там учатся"""
    try:
        for grade in list_grades:
            grade1 = session.query(Grade).filter_by(name=str(grade)).first()
        # Ищем есть класс в БД если есть добавляем отношения, нет пропускаем идем в след. по списку
            if grade1 is not None:
                group_grade_relation = session.query(Group).filter_by(id=group_id).first()
                group_grade_relation.grades.append(grade1)
                session.add(group_grade_relation)
                session.commit()
    except AttributeError:
        print('Ошибка ввода данных')

def del_all_relation_group_grade(group_id: str) -> None:
    """Удаление всех отношений с этой группой по классам"""
    while session.query(Group).filter_by(id=group_id).first().grades:
        grade_del = session.query(Group).filter_by(id=group_id).first()
        grade_del.grades.clear()
        session.commit()

def get_groups_list_for_grade(grade_number:str) -> list:
    """Получаем список групп в которых ученики учатся в этих классах в школе"""
    stmt = select(Group).where(and_(
        Grade.name == grade_number,
        Group.id == group_mtm_grade.c.group_id,
        Grade.id == group_mtm_grade.c.grade_id,
        ))
    groups_list = session.execute(stmt).scalars().all()
    return groups_list

def get_groups_reservation_text(grade_number: str) -> str:
    """Получаем список групп в которых ученики учатся в этих классах в школе + номер id"""
    groups_list = get_groups_list_for_grade(grade_number=grade_number)
    groups_text = ''
    for group in groups_list:
        groups_text += f'{"- "*20}\n{is_place_group(group_id=group.id)}\n'
        groups_text += f'{group.id}. '
        groups_text += f'{get_class_time(group_id=group.id, is_edit=False)}'
    return groups_text


# print(get_groups_reservation_text(1))

# print(get_user_free())
# print(get_schedule_teacher(1))

# print(session.query(Group).filter_by(id=1).first())



# print(get_group_list(schedule=True))

# start_times = datetime(year=2021, month=11, day=1, hour=11, minute=10)
# end_times = datetime(year=2021, month=11, day=7, hour=12, minute=45)
# print(check_class_time_busy(start_time=start_times, end_time=end_times, class_room_id=1, group_id=1))