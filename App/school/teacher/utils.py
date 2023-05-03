from school.models import Teacher
from school import db
from school.tools.utils import color
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

'''
Create an Endpoint with the following:
Create getTeacher function in order to get teacher data (teacher.utils.py)
1.- Get the relations Group-Teacher
2.- Get all the teacher data

Accepted filters:
    By id (id=int)
    Get all teacher DB registers (filter = all)
    By Subject (filter = subject)
    
Examples
{"id":1} This filter will return the teacher data with the selected id
{"filter":"all"} This filter will return all teachers in DB
{"filter":"Algoritmos"} This filter will return all the teachers that teach that subject
'''

def filter_Teacher(filterParams: str) -> list[dict]:
    try:
        if 'filter' in filterParams:
            if filterParams['filter'] == 'all':
                teachers = Teacher.query.all()
            else:
                teachers = Teacher.query.filter_by(
                    subject=filterParams['filter']).all()
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