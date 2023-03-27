from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from school import db
from school.tools.utils import color
from school.models import Group, User, Schedule, Classroom, Days, Hours
from school.classrooms.utils import createClassroom, createClassroomSubjectRelationship
from school.days.utils import *
from school.hours.utils import *
from datetime import datetime
import traceback
import logging
import re


def createSchedule(daysHours: list[str], classrooms: list[Classroom], group: Group) -> Schedule:
    '''Creates a schedule taking the days and hours from the schedule content and the classroom and groups objects'''
    try:

        if len(daysHours) != 0 and group:
            for i in range(len(daysHours)):

                schedule = Schedule(
                    # Dia: str
                    day=daysHours[i][0:str(daysHours[i]).index(' ')],
                    startTime=f"{int(daysHours[i][daysHours[i].index(' ') + 1:daysHours[i].index(':')]) + 12 if int(daysHours[i][daysHours[i].index(' ') + 1:daysHours[i].index(':')]) != 12 else int(daysHours[i][daysHours[i].index(' ') + 1:daysHours[i].index(':')])}:" \
                    f"{daysHours[i][daysHours[i].index(' ') + 1:daysHours[i].index('-') - 1][-6:-4]}:00" \
                    if 'p' in daysHours[i][daysHours[i].index(' ') + 1:daysHours[i].index('-') - 1] \

                    else f"{daysHours[i][daysHours[i].index(' ') + 1:daysHours[i].index(':')]}:" \
                    f"{daysHours[i][daysHours[i].index(' ') + 1:daysHours[i].index('-') - 1][-6:-4]}:00",  # Hora de inicio: datetime

                    endTime=f"{int(daysHours[i][daysHours[i].index('-') + 1:daysHours[i].rindex(':')]) + 12 if int(daysHours[i][daysHours[i].index('-') + 1:daysHours[i].rindex(':')]) != 12 else daysHours[i][daysHours[i].index('-') + 1:daysHours[i].rindex(':')]}:" \
                    f"{daysHours[i][daysHours[i].index('-') + 1:][-6:-4]}:00" \
                    if 'p' in daysHours[i][daysHours[i].index('-') + 1:] \
                    else f"{int(daysHours[i][daysHours[i].index('-') + 1:daysHours[i].rindex(':')])}:" \
                    f"{daysHours[i][daysHours[i].index('-') + 1:][-6:-4]}:00",
                    classroomID=classrooms[i]
                )

                db.session.add(schedule)
                db.session.commit()

                createScheduleGroupRelation(group, schedule)

        else:
            raise ValueError(
                f'{color(1,"Schedule creation failed")} ❌'
            )

    except Exception as e:
        logging.critical(
            f'{color(5,"Schedule creation failed")} ❌: {e}\n{traceback.format_exc().splitlines()[-3]}')
        schedule = None

    return schedule


def createScheduleGroupRelation(group: Group, schedule: Schedule) -> None:
    '''Create a relation between schedule and group in DB'''
    try:
        if group and schedule:
            if schedule not in group.schedule:
                group.schedule.append(schedule)
                db.session.commit()
                logging.info(f'{color(4,"Schedule relation created")} ✅')
            else:
                logging.info(
                    f'{color(4,"Schedule relation already exists")} ✅')
        else:
            raise ValueError(
                f'{color(1,"Schedule relation creation failed")} ❌'
            )
    except Exception as e:
        logging.critical(
            f'{color(5,"Schedule relation creation failed")} ❌: {e}\n{traceback.format_exc().splitlines()[-3]}')

# def getUserSubjects(user: User) -> dict:
#     '''Returns the user subjects as a dictionary with his subjects'''
# #     try:

# #         subjects = (
# #             db.session.query(Subject)
# #             .filter(Subject.id.in_((
# #                 db.session.query(RelationUserSubjectTable.c.subjectId)
# #                 .filter(RelationUserSubjectTable.c.studentId == user.id)
# #                 .subquery()
# #             )
# #             ))
# #             .all()
# #         )
# #         user = {'User': getUser(user)}
# #         user['User']['Subjects'] = list(map(
# #             lambda subject: getSubject(subject), subjects))
# #         logging.info(f"{color(2,'Get User Subjects Complete')} ✅")
# #     except Exception as e:
# #         logging.error(
# #             f"{color(1,'Get User Subjects Failed')} ❌: {e}\n{traceback.format_exc().splitlines()[-3]}")
# #         user = None
# #     return user


def getSchedule(Schedule: int) -> Schedule:
    '''Returns a object of type schedule given an id'''
    try:
        schedule = Schedule.query.filter_by(id=Schedule.id).first().toDict()
        if schedule:
            logging.info(f'{color(4,"Schedule found")} ✅')
        else:
            logging.warning(f'{color(1,"Schedule not found")} ❌')
    except Exception as e:
        logging.critical(
            f'{color(5,"Schedule not found")} ❌: {e}\n{traceback.format_exc().splitlines()[-3]}')
        schedule = None

    return formatDateObjsSchedule(schedule)


def formatDateObjsSchedule(schedule: dict[str:str]) -> dict[str:str]:
    '''Formats the date objects in the schedule dictionary'''
    # Format the date objects in the dictionary
    schedule['creationDate'] = schedule['creationDate'].strftime(
        '%Y-%m-%d %H:%M:%S')
    schedule['lastupDate'] = schedule['lastupDate'].strftime(
        '%Y-%m-%d %H:%M:%S')
    schedule['startTime'] = schedule['startTime'].strftime("%H:%M:%S")
    schedule['endTime'] = schedule['endTime'].strftime("%H:%M:%S")
    return schedule


# def findScheduleTable(browser):
#     try:
#         scheduleContent = browser.find_element(By.ID, "contenido-tabla")
#         logging.info(f'{color(2,"Schedule content found")} ✅')
#     except NoSuchElementException:
#         logging.error(f'{color(1,"Schedule content not found")} ❌')
#     return scheduleContent


# def findScheduleSubjects(scheduleContent: str) -> list[str]:
#     '''Extracts the schedule subjects from the schedule content'''
#     try:
#         rows = scheduleContent.find_elements(By.CSS_SELECTOR, "div.row")
#         logging.info(f'{color(4,f"Schedule content has {len(rows)} rows")}🔎')
#     except NoSuchElementException:
#         logging.warning(f'{color(1,"Schedule content has no rows")} ❌')

#     return [[cell.text for cell in row.find_elements(
#         By.CSS_SELECTOR, 'div')] for row in rows]


# def cleanScheduleData(subjectsList: list[list[Subject]]) -> list[dict[str, str]]:
#     '''Cleans the schedule data'''

#     return [
#         {
#             'day': subjectData[1].strip(),
#             'start_time': subjectData[2].strip(),
#             'end_time': subjectData[3].strip(),
#             'subject': subjectData[4].strip(),
#             'teacher': subjectData[6].strip(),
#             'start_date': subjectData[7].strip(),
#             'end_date': subjectData[8].strip(),
#             'group': subjectData[9].strip(),
#             'classroom': re.compile(r'([^/]*)$').search(re.sub(r'\n', '', subjectData[5].strip())).group(1).replace('Ver', '').lstrip()
#         }
#         for subjectData in subjectsList
#     ]


# def loadScheduleData(scheduleSubjects: list[dict[str, str]]) -> None:
#     '''Loads the schedule data into a Subject object'''
#     current_day = ''
#     subjects = [subject for subject in scheduleSubjects if subject != []]
#     try:
#         subject_data = cleanScheduleData(subjects)
#         for data in subject_data:
#             data['day'] = data['day'] if data['day'] else current_day
#             createSchedule(**data)
#             current_day = data['day']
#         logging.info(f'{color(4,"Schedule data loaded into DB")} ✅')
#     except Exception as e:
#         logging.error(
#             f'{color(1,"Schedule data not loaded into DB")} ❌: {e}\n{traceback.format_exc().splitlines()[-3]}')


# def createSchedule(day: str, start_time: datetime, end_time: datetime, subject: str, teacher: str, start_date: datetime, end_date: datetime, group: str, classroom: str) -> None:
#     '''Creates a schedule object'''

#     # create objects
#     subject = createSubject(day, start_time, end_time, subject, teacher,
#                             start_date, end_date, group)
#     classroom = createClassroom(classroom)
#     # create relations

#     # createUserSubjectRelationship(User.query.filter_by(
#     #     userID=session['user']['userID']).first(), subject)


# def fetchScheduleContent(browser: ChromeBrowser) -> None:
#     '''Extracts the schedule content from the schedule page and returns a list of dictionaries with the schedule data'''
#     try:
#         loadScheduleData(
#             findScheduleSubjects(findScheduleTable(browser)))
#     except Exception as e:
#         logging.error(
#             f"{color(1,'Schedule content not extracted')} ❌: {e}\n{traceback.format_exc().splitlines()[-3]}")


# def createCompatibleSchedule(subjects: Subject) -> list[Subject]:
#     '''Creates a compatible schedule for the user based on the subjects in database'''
#     try:
#         days = {"Lunes": 0, "Martes": 1, "Miércoles": 2,
#                 "Jueves": 3, "Viernes": 4, "Sábado": 5, "Domingo": 6}
#         sorted_subjects = sorted(subjects, key=lambda subject: (
#             days[subject.day], subject.startTime))

#         schedule = [getSubject(sorted_subjects[i])
#                     for i in range(len(sorted_subjects))]

#         # create a list of days

#     except Exception as e:
#         logging.error(
#             f"{color(1,'Compatible Schedule Not Created')} ❌: {e}\n{traceback.format_exc().splitlines()[-3]}")
#         schedule = None
#     return schedule

def combinations_of_courses(BDlist: list) -> list:

    def decimal_to_base(number, maximum, list_length):
        b = ''
        while True:
            a = number % maximum
            b = str(a) + b
            number = number // maximum
            if number == 0:
                break

        if len(b) < list_length:
            b = '0' * (list_length - len(b)) + b
        # else:
        #     b = b[-list_length:]
        return b

    max_element = max([len(element) for element in BDlist])
    combinations = max_element ** len(BDlist)
    base_combinations = []

    for n in range(combinations):
        base_combinations.append(decimal_to_base(n, max_element, len(BDlist)))
    courses_combinations = []

    for combination in base_combinations:
        courses_combinations.append([])
        for i, element in enumerate(combination):
            try:
                courses_combinations[-1].append(BDlist[i][int(element)])
            except IndexError:
                courses_combinations[-1].append('~')

    courses_combinations = [x for x in courses_combinations if '~' not in x]

    return courses_combinations


def cleanData(list_of_courses: list) -> list:
    '''Cleans the data from the database'''
    
    distinct_courses = list(set([course['subject'] for course in list_of_courses]))
    distinct_courses.sort()
    BD_list_of_courses = []       
    
    for course in distinct_courses:
        BD_list_of_courses.append([])
        for course_ in list_of_courses:
            if course == course_['subject']:
                BD_list_of_courses[-1].append(course_)
    
    list_of_courses = BD_list_of_courses
        
    return list_of_courses

def validateSchedule(schedules: list) -> list:
    '''Validates the schedules that don't have any conflicts'''
    valid_schedules = []
    for schedule in schedules:
        days = {}
        for indx, subject in enumerate(schedule):
            for course in subject['Schedules']:
                if sum(1 for c in course['day'] if c.isupper()) > 1:
                    separated_days = re.findall('[A-Z][^A-Z]*', course['day'])
                    for day in separated_days:
                        if day not in days:
                            days[day] = []
                else:
                    if course['day'] not in days:
                        days[course['day']] = []
                        
                if sum(1 for c in course['day'] if c.isupper()) > 1:
                    separated_days = re.findall('[A-Z][^A-Z]*', course['day'])
                    for day in separated_days:
                        days[day].append(course)
                else:
                    days[course['day']].append(course)
                    
        for day in days:
            for indx, course in enumerate(days[day]):
                for indx_, course_ in enumerate(days[day]):
                    if indx != indx_:
                        if course['startTime'] < course_['startTime'] < course['endTime'] or course['startTime'] < course_['endTime'] < course['endTime']:
                            break
                else:
                    continue
                break
            else:
                continue
            break
        else:
            valid_schedules.append(schedule)
                        
    return valid_schedules
