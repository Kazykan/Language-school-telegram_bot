"""Машина состояний для работы опросников"""
from aiogram.dispatcher.filters.state import StatesGroup, State


class GroupStatesGroup(StatesGroup):
    """Машина состояний для работы опросника по добавлению Группы в БД"""
    name = State()
    quota = State()
    price = State()
    duration = State()
    description = State()
    grade = State()
    teacher_id = State()


class UserStatesGroup(StatesGroup):
    """Машина состояний для работы опросника по добавлению ученика в БД"""
    first_name = State()
    last_name = State()
    town = State()
    description = State()
    birthday = State()
    phone_number = State()
    group_id = State()


class ClassTimeStatesGroup(StatesGroup):
    """Машина состояний для работы опросника по добавлению времени занятий в БД"""
    group_id = State()
    class_room_id = State()
    start_time = State()
