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