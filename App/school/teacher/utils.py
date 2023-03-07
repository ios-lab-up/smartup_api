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
            raise ValueError(
                f'{color(3,"Teacher already exists in database")}, {name}')
    except Exception as e:
        logging.error(
            f'{color(1,"Couldnt create teacher")} ❌: {e} {traceback.format_exc().splitlines()[-3]}')
        teacher = Teacher.query.filter_by(name=name).first()

    return teacher
