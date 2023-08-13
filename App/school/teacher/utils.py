from ..models import Teacher
from ..models import Group
from .. import db
from ..tools.utils import color
import logging
import traceback


def createTeacher(name: str) -> Teacher:
    '''Creates a teacher object'''

    try:
        # Check if teacher already exists in database
        if not Teacher.query.filter_by(name=name).first():
            # Create teacher object if it doesn't exist in database
            teacher = Teacher(name=name)
            # Add teacher to database
            db.session.add(teacher)
            db.session.commit()
            logging.info(f'{color(2,"Teacher created")} ✅')
        else:
            # Raise an error if teacher already exists in database
            teacher = Teacher.query.filter_by(name=name).first()
            raise ValueError(
                f'{color(3,"Teacher already exists in database")}, {name}')
    except Exception as e:
        logging.error(
            f'{color(1,"Couldnt create teacher")} ❌: {e} {traceback.format_exc().splitlines()[-3]}')
        teacher = Teacher.query.filter_by(name=name).first()

    return teacher

def subjectTeacher(subjectid: int) -> list[dict]:
    '''Returns a list of teachers that teach a specific subject
    '''
    try:
        # search the subject in Subject data base
        groups=Group.query.filter_by(subject= subjectid).all()
        teachers=[]
        for group in groups:
            teacherfilter={
            "id":f"{group.teacher}"
            }
            teacher=filter_Teacher(teacherfilter)
            teachers.append(teacher)
        logging.info(f'{color(2,"Teachers found")} ✅')
    except Exception as e:
        logging.error(
            f'{color(1,"Couldnt find teachers")} ❌: {e} {traceback.format_exc().splitlines()[-3]}')
        teachers = None

    return teachers

def filter_Teacher(filterParams: str) -> list[dict]:
    try:
        if 'filter' in filterParams:
            if filterParams['filter'] == 'all':
                teachers = Teacher.query.all()
            else:
                teachers=subjectTeacher(filterParams['filter'])
        elif 'id' in filterParams:
            teachers = Teacher.query.filter_by(id=filterParams['id']).all()
        else:
            raise ValueError(
                f'{color(3,"Invalid filter")} ❌: {filterParams}')
    except Exception as e:
        logging.error(
            f'{color(1,"Couldnt filter teacher")} ❌: {e} {traceback.format_exc().splitlines()[-3]}')
        teachers = None
    return teachers