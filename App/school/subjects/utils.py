from school import db
from school.models import Subject, ChromeBrowser, Teacher, Classroom
from school.tools.utils import color
from school.groups.utils import createGroup
from school.teacher.utils import createTeacher
from school.classrooms.utils import createClassroom
from school.schedule.utils import createSchedule
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import re
import logging
import traceback


def createSubject(name: str):
    '''Creates a subject object'''
    try:

        if not Subject.query.filter_by(name=name).first():
            subject = Subject(name=name)
            # Subject(day=day, startTime=start_time, endTime=end_time, name=subject, teacher=teacher,
            #                   startDate=datetime.strptime(start_date, '%d/%m/%Y'), endDate=datetime.strptime(end_date, '%d/%m/%Y'), group=group, )

            db.session.add(subject)
            db.session.commit()
            logging.info(f"{color(2,'Subject created:')} ✅")
        else:
            raise ValueError(
                f"{color(3,'Subject already exists in the database')}")
    except Exception as e:
        logging.error(
            f"{color(1,'Subject not created')} ❌: {e}\n{traceback.format_exc().splitlines()[-3]}")
        subject = Subject.query.filter_by(name=name).first()
    return subject


def getSubject(subject: Subject) -> dict[str, str]:
    '''Returns the subject data as a dictionary'''
    subjects = Subject.to_dict(Subject.query.filter_by(id=subject.id).first())
    logging.info(f"{color(2,'Get Subject Complete')} ✅")
    return formatDateObjsSubject(subjects)


def formatDateObjsSubject(subjects: dict[str, str]) -> dict[str, str]:
    '''Formats the date objects in the subject dictionary'''
    subjects['startDate'] = subjects['startDate'].strftime('%Y-%m-%d')
    subjects['endDate'] = subjects['endDate'].strftime('%Y-%m-%d')
    subjects['startTime'] = subjects['startTime'].strftime('%H:%M')
    subjects['endTime'] = subjects['endTime'].strftime('%H:%M')
    subjects['creationDate'] = subjects['creationDate'].strftime(
        '%Y-%m-%d %H:%M:%S')
    subjects['lastupDate'] = subjects['lastupDate'].strftime(
        '%Y-%m-%d %H:%M:%S')
    return subjects


def extractSubjectsFromTable(browser: ChromeBrowser) -> list[str]:
    '''Once the html table was located, it scrappes the subjects out
       of it and returns a list of list, each list represents a subject '''
    try:
        # var is used to iterate over the rows of the table
        rows = browser.find_elements(
            By.XPATH, f'//*[@id="ACE_$ICField$4$$0"]/tbody/tr')

        logging.info(
            f"{color(2,'Subjects content found')} ✅")
        logging.info(
            f"{color(4,f' Subjects found')} 🔎")
    except NoSuchElementException:
        logging.error(
            f"{color(1,'Subjects content not found')} ❌")

    return rows


def splitListCourses(rows: list[str]) -> list[list[str]]:
    '''Given a list of courses, it splits them into a list of lists, each list represents a course'''
    # The try-except block is used to catch any errors that may occur and log them
    try:
        # The map() function returns a list of the results after applying the given function to each item of a given iterable (list, tuple etc.)
        # In this case, the given function is the lambda function, which splits the text of each row using the new line character (\n) as a separator
        # The result of this is a list of lists, each sublist contains the text of each row
        subjectData = [[line.strip() for line in row.text.splitlines() if line.strip() != '']
                       for row in rows if rows != []]
        separated_classes = []
        current_group = []
        # The for loop iterates over each list in the subjectData list and stores the result of each iteration in the sub_list variable
        for sub_list in subjectData:
            # The for loop iterates over each element in the sub_list variable and stores the result of each iteration in the item variable
            for item in sub_list:
                # The if statement verifies that the item variable is not equal to the string "Clase Sección Días y Horas Aula Instructor Idioma Inscr / Cap Estado      "
                if item != "Clase Sección Días y Horas Aula Instructor Idioma Inscr / Cap Estado":
                    # If the condition is true, the item variable is appended to the current_group list
                    current_group.append(item)
                else:
                    # If the condition is false, the if statement verifies that the current_group list is not empty
                    if current_group:
                        # If the condition is true, the current_group list is appended to the separated_classes list
                        separated_classes.append(current_group)
                    # The current_group list is reset to a list containing the first element of the sub_list variable
                    current_group = [sub_list[0]]
            # The if statement verifies that the current_group list is not empty
            if current_group:
                # If the condition is true, the current_group list is appended to the separated_classes list
                separated_classes.append(current_group)
            # The current_group list is reset to an empty list
            current_group = []

        cleanedSubjectData = [
            classes for classes in separated_classes if len(classes) > 1]

        logging.info(
            f"{color(2,'Courses split successfully')} ✅")
    # If an error occurs, the except block is executed
    except Exception as e:
        logging.error(
            f"{color(1,'Courses not split')} ❌: {e}\n{traceback.format_exc().splitlines()[-3]}")
    # The function returns a list containing only the courses in separated_classes that have more than one element
    # add language to the end of each list

    return cleanedSubjectData


def fetchGroupData(browser: ChromeBrowser) -> list[str]:
    '''Fetches the subject data from the html'''
    groups: list[str] = []
    extractedHTML: list[str] = extractSubjectsFromTable(browser)
    subjectData: list[list[str]] = splitListCourses(
        extractedHTML)
    # print(subjectData)
    languages: list[str] = fetchLanguages(browser, len(subjectData))

    # add language to the end of each list
    for i in enumerate(subjectData):
        subjectData[i[0]].append(languages[i[0]])

    # add days and times to the end of each list
    for subjectElement in subjectData:

        subject = createSubject(subjectElement[0])
        teacher = fetchTeachers(subjectElement)
        classrooms = [classroom.id for classroom in (createClassroom(
            classroomObj) for classroomObj in fetchClassroom(subjectElement)) if classroom is not None]

        dayshours = fetchDateTime(subjectElement)

        group = createGroup(subject=subject.id, classNumber=subjectElement[1], group=subjectElement[2].split(
            '-')[0], teacher=teacher.id, language=subjectElement[-1], students=getStudentRoom(subjectElement),
            modality=fetchModality(subjectElement), description=fetchDescription(subjectElement))

        createSchedule(dayshours, classrooms, group)

        groups.append(group)

    return groups


def getStudentRoom(data: list[list[str]]) -> str:
    '''Gets the student room'''
    try:
        for studentRoom in data:
            if re.search(r'\d{2}/\d{2}|\d{1}/\d{1}|\d{1}/\d{2}', studentRoom):
                return studentRoom
    except Exception as e:
        logging.error(
            f"{color(1,'Student room not found')} ❌: {e}\n{traceback.format_exc().splitlines()[-3]}")
        return ''


def fetchModality(data: list[list[str]]) -> str:
    '''Fetches the modality from the lists'''
    try:
        for modality in data:
            if modality.startswith('Pres') or modality.startswith('En l'):
                return modality
            else:
                pass
    except Exception as e:
        logging.error(
            f"{color(1,'Modality not found')} ❌: {e}\n{traceback.format_exc().splitlines()[-3]}")
        return ''


def fetchDescription(data: list[list[str]]) -> str:
    '''Fetches the description from the lists'''
    try:
        for description in data:
            if description.startswith('Notas:'):
                return description
            elif description.startswith('Se prevé'):
                return description
            else:
                pass
    except Exception as e:
        logging.error(
            f"{color(1,'Description not found')} ❌: {e}\n{traceback.format_exc().splitlines()[-3]}")
        return ''


def fetchTeachers(data: list[list[str]]) -> Teacher:
    '''Fetches the teachers from the lists'''
    teachers = []
    substrings = ('Clase', 'Sección', 'Notas:', 'Sala ', 'Salón', 'Se prevé', 'Todas',
                  'Presencial', 'Personal', 'En l', 'Español', 'Lun', 'Mart', 'Jue', 'Miérc', 'V', 'Sáb', 'Lab')
    try:
        for teacher in data[::-1]:
            if any(teacher.startswith(substring) for substring in substrings) or re.search(r'\d{2}/\d{2}|\d{1}/\d{1}|\d{1}/\d{2}', teacher) or re.search(r'\d', teacher):
                pass
            else:
                teachers.append(teacher)
                break

        for teacherData in list(set(teachers)):
            teacher = createTeacher(teacherData)
        logging.info(
            f"{color(2,'Teacher fetched successfully')} ✅")
    except Exception as e:
        logging.error(
            f"{color(1,'Teacher not fetched')} ❌: {e}\n{traceback.format_exc().splitlines()[-3]}")

    return teacher


def fetchLanguages(browser: ChromeBrowser, subjects: int) -> list[str]:
    languagesList = []
    try:
        for subject in range(subjects):
            languages = browser.find_element(
                By.XPATH, f'//*[@id="win0divUP_DERIVED_IDM_UP_CLASS_LANG${subject}"]')
            match = re.search(
                r'src="(.*?)"', languages.get_attribute('innerHTML'))
            if match and match.group(1).split('/')[-1] == 'PS_MEX_COL_ESP_1.gif':
                languagesList.append('Español')
            elif match and match.group(1).split('/')[-1] == 'PS_USA_COL_ESP_1.gif':
                languagesList.append('Inglés')
            else:
                languagesList.append('No especificado')
    except Exception as e:
        logging.error(
            f"{color(1,'Languages not fetched')} ❌: {e}\n{traceback.format_exc().splitlines()[-3]}")
    return languagesList


def fetchDateTime(data: list[list[str]]) -> list[str]:
    '''Gets the date and time from the lists'''
    try:
        dateTimeStrings = [
            info for info in data if ":" in info and " - " in info]

    except Exception as e:
        logging.error(
            f"{color(1,'Date and time not found')} ❌: {e}\n{traceback.format_exc().splitlines()[-3]}")
        return ''
    return dateTimeStrings


def fetchClassroom(data: list[list[str]]) -> list[str]:
    '''Gets the classroom from the lists'''
    try:
        classrooms = [
            info for info in data if "Sala " in info or "Salón" in info or "Laboratorio" in info or "P/Asig" in info]
    except Exception as e:
        logging.error(
            f"{color(1,'Classroom not found')} ❌: {e}\n{traceback.format_exc().splitlines()[-3]}")
        return ''
    return classrooms
