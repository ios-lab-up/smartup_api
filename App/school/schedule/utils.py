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
    """Returns a list of lists with all the possible combinations of courses"""
    
    # This function is based on the decimal to base conversion algorithm, 
    # but instead of converting a decimal number to a base number, 
    # it converts a decimal number to a base number with a variable maximum value.
    
    # This function is the nucleus of the algorithm, it is the one that generates all the possible combinations of courses based on the courses that the user has in the database,
    # but it has a maximum number of courses per day, which is 10 (base 10), so it is necessary to convert the decimal number to a base number with a maximum value of 10.
    def decimal_to_base(number, maximum, list_length):
        """Converts a decimal number to a base number with a variable maximum value"""
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

    # We define the maximum number of courses, this is necessary because the algorithm needs to know in what base to convert the decimal number,
    # and the maximum number of courses will be the base.
    max_element = max([len(element) for element in BDlist])
    
    # We generate a number, wich is the number of possible combinations of courses, this number is the maximum number of courses to the power of the number of days.
    # C = MAX ** DAYS
    combinations = max_element ** len(BDlist)
    base_combinations = []

    # We generate a number in base n, where n is the maximum number of courses, and we convert it to decimal, this is done for each possible combination of courses.
    for n in range(combinations):
        # We store the decimal number in a list, this list will be the list base n numbers (000, 001, etc.)
        base_combinations.append(decimal_to_base(n, max_element, len(BDlist)))
    courses_combinations = []
    
    # After generating the list of base n numbers, we iterate over each number in the list and asign the corresponding course to each number.
    # Each number will be the index of the course in the list of courses of the day.
    for combination in base_combinations:
        # We create a list for each combination of courses.
        courses_combinations.append([])
        for i, element in enumerate(combination):
            try:
                # We append the course to the list of courses of the combination.
                courses_combinations[-1].append(BDlist[i][int(element)])
            except IndexError:
                # If the course does not exist, we add a ~ to the list, this is done to avoid errors when generating the schedules.
                courses_combinations[-1].append('~')
    # Finally, we remove the combinations that have a ~, this is done to avoid errors when generating the schedules.
    courses_combinations = [x for x in courses_combinations if '~' not in x]

    return courses_combinations


def cleanData(list_of_courses: list) -> list:
    '''Cleans the data from the database in order to generate the schedules'''
    
    # We create a list of distinct courses.
    distinct_courses = list(set([course['subject'] for course in list_of_courses]))
    # We sort it, so it will remain constant.
    distinct_courses.sort()
    BD_list_of_courses = []       
    
    # We iterate over the list of distinct courses and we create a list of lists, where each list contains the courses of the same subject.
    for course in distinct_courses:
        BD_list_of_courses.append([])
        for course_ in list_of_courses:
            if course == course_['subject']:
                BD_list_of_courses[-1].append(course_)
        
    return BD_list_of_courses

def validateSchedule(schedules: list) -> list:
    '''Validates the schedules that don't have any conflicts'''
    valid_schedules = []
    for schedule in schedules:
        # We start by creating a dictionary with the days of the week as keys and an empty list as values, we need to repeat this for each schedule.
        days = {}
        for indx, subject in enumerate(schedule):
            for course in subject['Schedules']:
                # There are some days in the database that are separated by a uppercase letter, so we need to separate them, to do this we need 
                # to know if the day has more than one uppercase letter, if it does, we separate it, if it doesn't, we don't.
                if sum(1 for c in course['day'] if c.isupper()) > 1:
                    separated_days = re.findall('[A-Z][^A-Z]*', course['day'])
                    for day in separated_days:
                        if day not in days:
                            days[day] = []
                # The day is not separated, so we add it to the dictionary.
                else:
                    if course['day'] not in days:
                        days[course['day']] = []
                
                # We add the course to the list of courses of its day.
                if sum(1 for c in course['day'] if c.isupper()) > 1:
                    separated_days = re.findall('[A-Z][^A-Z]*', course['day'])
                    for day in separated_days:
                        days[day].append(course)
                else:
                    days[course['day']].append(course)
        
        # We iterate over the days of the week, and for each day we iterate over the courses of the day, and for each course we iterate over the courses of the day again,
        # if the start time of the course is less than the start time of the other course and the end time of the course is greater than the start time of the other course,
        # or if the start time of the course is less than the end time of the other course and the end time of the course is greater than the end time of the other course,
        # then the course has a conflict, so we break the loop and go to the next schedule, if the course does not have a conflict, we continue with the next course.
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
            # If the schedule does not have any conflicts, we add it to the list of valid schedules.
            valid_schedules.append(schedule)
    
    # At this point, we have a list of valid schedules, so we return it.
    return valid_schedules
