"""Основлной модуль с инициализацией БД и полями БД"""

from datetime import datetime
from sqlalchemy import Column, create_engine, Table, String, Integer, Text, DateTime,\
    Boolean, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship


engine = create_engine('sqlite:///sqlite3.db')

session = Session(bind=engine)
Base = declarative_base()
metadata = Base.metadata

"""Отношения многие ко многим группы и класс ученика который учатся в этих группах"""
group_mtm_grade = Table('group_grade', Base.metadata,
                    Column('group_id', ForeignKey('group.id')),
                    Column('grade_id', ForeignKey('grade.id')))


class Teacher(Base):
    """Учитиля"""
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
    
    teacher_id = Column(Integer(), ForeignKey("teacher.id"))
    teacher = relationship('Teacher', backref="group")
    grades = relationship('Grade', secondary=group_mtm_grade, backref='group')

    def __repr__(self) -> str:
        return f'{self.name} {self.get_grades_txt()}'
    
    def get_grades_list(self) -> list:
        """Получаем списком классы которые относяться к этой группе"""
        grades_data = session.query(Group).filter_by(id=self.id).first().grades
        return grades_data
    
    def get_grades_txt(self) -> str:
        """Получаем текстом классы которые относяться к этой группе"""
        grade_text = ", ".join(map(str, self.get_grades_list()))
        return f'({grade_text} классы)'


class Grade(Base):
    """Класс в котором учиться ученик, 0 - дошкольник, 12 - студент, 13 - взрослый"""
    __tablename__ = 'grade'
    id = Column(Integer(), primary_key=True)
    name = Column(Integer(), nullable=False)

    def __repr__(self) -> str:
        return f'{self.name}'


class User(Base):
    """Ученики"""
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
    """Кабинет может быть онлайн"""
    __tablename__ = 'class_room'
    id = Column(Integer(), primary_key=True)
    name = Column(String(100), nullable=False)
    location = Column(String(20),  nullable=False)
    description = Column(Text())


class ClassTime(Base):
    """Время занятий, занятия могут идти одна за одной"""
    __tablename__ = 'class_time'
    id = Column(Integer(), primary_key=True)
    start_time = Column(DateTime(), nullable=False)
    end_time = Column(DateTime(), nullable=False)

    group_id = Column(Integer(), ForeignKey("group.id"))
    group = relationship('Group', backref="class_time")
    class_room_id = Column(Integer(), ForeignKey('class_room.id'))
    class_room = relationship('ClassRoom', backref="class_time")


Base.metadata.create_all(engine)