from school.models import User, Subject
from school import db
from school.tools.utils import color
from flask import session
import logging
import traceback


def createUser(userID: str, password: str, name: str) -> User:
    '''Creates a user object'''
    # Check if user already exists in database
    try:
        if not User.query.filter_by(userID=userID).first():
            # Create user object if it doesn't exist in database

            user = User(
                userID=userID,
                password=password,
                name=name.split(' ')[0],
                lastName=' '.join(name.split(' ')[1:]),
                email=userID+"@up.edu.mx",
                profileID=3 if userID.isnumeric() else 5
            )
            # Add user to database
            db.session.add(user)
            db.session.commit()
            logging.info(f'{color(2,"User created")} ✅')
        else:
            # Raise an error if user already exists in database
            raise ValueError(
                f'{color(3,"User already exists in database")}')
    except Exception as e:
        logging.error(
            f'{color(1,"Couldnt create user")} ❌: {e} {traceback.format_exc().splitlines()[-3]}')
        user = None

    return user


def createUserSubjectRelationship(user: User, subject: Subject) -> None:
    '''Creates a relationship between a user and a subject by adding the subject to the user's subjects list'''

    try:
        # Check if the user or subject exist in the database
        # Get the user and subject objects from the database
        checkUser = User.query.filter_by(id=user.id).first()
        checkSubject = Subject.query.filter_by(id=subject.id).first()

        # Check if the user and subject objects exist
        if checkUser and checkSubject:
            # Check if the relationship already exists
            if subject not in user.subjects:
                # Append the subject object to the user subjects list
                user.subjects.append(subject)
                # Commit the changes to the database
                db.session.commit()
                # Log the successful completion of the task
                logging.info(
                    f'{color(2,"User-Subject relationship created")} ✅')
            else:
                # Log the error
                raise ValueError(
                    logging.error(
                        f'{color(3,"User-Subject relationship already exists")} ❌'))
        else:
            # Log the error
            raise TypeError(
                logging.error(
                    f'{color(1,"User or subject not found in database")} ❌'))
    except Exception as e:
        logging.error(
            f'{color(1,"Couldnt create user-subject relationship")} ❌: {e} {traceback.format_exc().splitlines()[-3]}')


def getUser(userID: User, type: int) -> User:
    '''Returns a list with the group data by passing an ID
       type: 1 = list
             2 = dict
    '''
    try:
        user = User.query.filter_by(id=userID).first()
        match type:
            case 1:
                userData = user
            case 2:
                userData = user.toDict()
                userData['jwt_token'] = session['user']['jwt_token']

    except Exception as e:
        logging.error(
            f'{color(1,"Couldnt get user")} ❌: {e} {traceback.format_exc().splitlines()[-3]}')
        userData = None
    return userData


def formatDateObjsUser(user: dict[str:str]) -> dict[str:str]:
    '''Formats the date objects in the user dictionary'''
    # Format the date objects in the dictionary
    user['created_at'] = user['creationDate'].strftime(
        '%Y-%m-%d %H:%M:%S')
    user['lastupDate'] = user['lastupDate'].strftime('%Y-%m-%d %H:%M:%S')
    return user
