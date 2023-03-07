from school.models import Student, Subject
from school import db
from school.tools.utils import color
import logging
import traceback


def createStudent(studentID: str, password: str, name: str) -> Student:
    '''Creates a student object'''
    # Check if student already exists in database
    try:
        if not Student.query.filter_by(studentID=studentID).first():
            # Create student object if it doesn't exist in database
            student = Student(
                studentID=studentID,
                password=password,
                name=name.split(' ')[0],
                lastName=' '.join(name.split(' ')[1:]),
                email=studentID+"@up.edu.mx"
            )
            # Add student to database
            db.session.add(student)
            db.session.commit()
            logging.info(f'{color(2,"Student created")} ✅')
        else:
            # Raise an error if student already exists in database
            raise ValueError(
                f'{color(3,"Student already exists in database")}')
    except Exception as e:
        logging.error(
            f'{color(1,"Couldnt create student")} ❌: {e} {traceback.format_exc().splitlines()[-3]}')
        student = None

    return student


def createStudentSubjectRelationship(student: Student, subject: Subject) -> None:
    '''Creates a relationship between a student and a subject by adding the subject to the student's subjects list'''

    try:
        # Check if the student or subject exist in the database
        # Get the student and subject objects from the database
        checkStudent = Student.query.filter_by(id=student.id).first()
        checkSubject = Subject.query.filter_by(id=subject.id).first()

        # Check if the student and subject objects exist
        if checkStudent and checkSubject:
            # Check if the relationship already exists
            if subject not in student.subjects:
                # Append the subject object to the student subjects list
                student.subjects.append(subject)
                # Commit the changes to the database
                db.session.commit()
                # Log the successful completion of the task
                logging.info(
                    f'{color(2,"Student-Subject relationship created")} ✅')
            else:
                # Log the error
                raise ValueError(
                    logging.error(
                        f'{color(3,"Student-Subject relationship already exists")} ❌'))
        else:
            # Log the error
            raise TypeError(
                logging.error(
                    f'{color(1,"Student or subject not found in database")} ❌'))
    except Exception as e:
        logging.error(
            f'{color(1,"Couldnt create student-subject relationship")} ❌: {e} {traceback.format_exc().splitlines()[-3]}')


def getStudent(student: Student) -> dict[str:str]:
    '''Returns a dictionary with the student's information'''
    # Create a dictionary with the student's information
    try:
        students = Student.to_dict(
            Student.query.filter_by(id=student.studentID).first())
        logging.info(f'{color(2,"Get Student Complete")} ✅')
    except Exception as e:
        logging.error(
            f'{color(1,"Couldnt get student")} ❌: {e} {traceback.format_exc().splitlines()[-3]}')
        students = None
    return formatDateObjsStudent(students)


def formatDateObjsStudent(student: dict[str:str]) -> dict[str:str]:
    '''Formats the date objects in the student dictionary'''
    # Format the date objects in the dictionary
    student['created_at'] = student['creationDate'].strftime(
        '%Y-%m-%d %H:%M:%S')
    student['lastupDate'] = student['lastupDate'].strftime('%Y-%m-%d %H:%M:%S')
    return student
