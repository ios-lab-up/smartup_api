from ..models import Classroom, Subject
from .. import db
from ..tools.utils import color
import logging
import traceback

def create_classroom(name: str) -> Classroom:
    """Creates a classroom object"""

    try:
        # Check if classroom already exists in a database
        if not Classroom.query.filter_by(name=name).first():
            # Create a classroom object if it doesn't exist in a database
            classroom = Classroom(name=name)
            # Add classroom to database
            db.session.add(classroom)
            db.session.commit()
            logging.info(f'{color(2,"Classroom created")} ✅')

        else:
            Classroom.query.filter_by(name=name).first()
            # Raise an error if a classroom already exists in a database
            raise ValueError(
                f'{color(3,"Classroom already exists in database")}'
            )
    except Exception as e:
        logging.error(
            f'{color(1,"Could not create classroom")} ❌: {e} {traceback.format_exc().splitlines()[-3]}')
        classroom = Classroom.query.filter_by(name=name).first()

    return classroom


def create_classroom_subject_relationship(classroom: Classroom, subject: Subject) -> None:
    """Creates a relationship between a subject and a classroom
    by adding the classroom to the subject's classroom list"""

    try:
        if classroom and subject:
            # Check if the relationship already exists
            if subject not in classroom.subjectsClasroom:
                # Append the classroom object to the subject classrooms list
                classroom.subjectsClasroom.append(subject)
                # Commit the changes to the database
                db.session.commit()
                # Log the successful completion of the task
                logging.info(
                    f'{color(2,"Classroom-Subject relationship created")} ✅')
            else:
                # Log the error
                raise ValueError(
                    logging.error(
                        f'{color(3,"Classroom-Subject relationship already exists")} ❌'
                    )
                )
        else:
            raise ValueError(
                logging.error(
                    f'{color(1,"Classroom or subject doesnt exist")} ❌'
                )
            )
    except Exception as e:
        logging.error(
            f'{color(1,"Could not create classroom-subject relationship")} ❌: {e} {traceback.format_exc().splitlines()[-3]}')
