from typing import Tuple, List

from .. import db
from ..models import Group, Schedule, Subject, Teacher
from ..relations import RelationGroupSchedule
from ..schedule.utils import  getSchedule
import logging
import traceback
from ..tools.utils import color


def create_group(class_number: int, group: str, subject: int, teacher: int, language: str, students: str, modality: str, description: str) -> Group:
    """Creates a group in the database"""
    try:
        if not Group.query.filter_by(classNumber=class_number).first():

            group = Group(
                classNumber=class_number,
                group=group,
                subject=subject,
                teacher=teacher,
                language=language,
                students=students,
                modality=modality,
                description=description,
                options=0,
                status=False if students.split('/')[0] == students.split('/')[1] else True
            )
            db.session.add(group)
            db.session.commit()
            logging.info(f"{color(2,'Group created:')} ✅")
        else:
            Group.query.filter_by(classNumber=class_number).first()
            raise Exception(f'{color(3,"Group already exists in database")}')

    except Exception as e:
        logging.error(
            f'{color(1,"Couldnt create group")} ❌: {e} {traceback.format_exc().splitlines()[-3]}')
        group = Group.query.filter_by(classNumber=class_number).first()

    return group


def getGroup(group_id: int, data_type: int) -> Group:
    """Returns a list with the group data by passing an ID
       type: 1 = list
             2 = dict
    """
    try:

        group = Group.query.filter_by(id=group_id).first()
        if group:

            group.schedules = db.session.query(Schedule)\
                .join(RelationGroupSchedule)\
                .filter(RelationGroupSchedule.c.groupId == group_id)\
                .all()
            
            match data_type:
                case 1:
                    group_data = group
                case 2:
                    group_data = group.toDict()
                    group_data['schedules'] = list(map(
                        lambda schedule: getSchedule(schedule), group.schedules))
                    group_data['subject'] = getattr(
                        Subject.query.filter_by(id=group.subject).first(), 'name')
                    group_data['teacher'] = getattr(
                        Teacher.query.filter_by(id=group.teacher).first(), 'name')
                case _:
                    raise Exception(f'{color(3,"Type not found")}')

        else:
            raise Exception(f'{color(3,"Group not found")}')

    except Exception as e:
        logging.error(
            f'{color(1,"Couldnt get group")} ❌: {e} {traceback.format_exc().splitlines()[-3]}')
        group_data = None
    
    return group_data


def cleanGroupQuery(schedule_list: list[Group]) -> list[Group]:
    """Returns a list without the groups that doesn't have empy schedules lists"""
    try:
        for group in schedule_list:
            if len(group.schedule) == 0:
                schedule_list.remove(group)
    except Exception as e:
        logging.critical(
            f'{color(5,"Schedule list cleaning failed")} ❌: {e}\n{traceback.format_exc().splitlines()[-3]}')
        
    return schedule_list


def filterGroups(filter_params: ...) -> tuple[list[Group] | None, str]:
    """
    Returns a list with the group data by passing an ID
    This function purpose is to filter groups by a given parameter and return a list of groups that match the filter criteria
    filterParams is a dictionary with the following structure:
    filterParams = {
      'id': 1,
      'subject': 'Math',
      'language': 'English',
      'dateRange': '2021-01-01,2021-01-31'
    }
    The function will return a list of groups that match the filter criteria
    but if the filterParams is empty or contains the key 'all' it will return all the groups in the database
    """
    try:

        filter_map = {
            'id': Group.id,
            'subject': Group.subject,
            'language': Group.language,
            'dateRange': Group.creationDate
        }
        message: str = ''
        criteria: str = ''
        if 'all' in filter_params:
            groups = Group.query.all()
            message = f'{len(groups)} Groups in DB'
        else:
            for key, value in filter_params.items():
                if key == 'dateRange':
                    start_date, end_date = value.split(',')
                    query = Group.query.filter(
                        filter_map[key].between(start_date, end_date)
                    )
                    criteria = f"Date range: {start_date} - {end_date}"
                elif key == 'subjects':
                    # Return all the groups that contain the id given a list
                    query = Group.query.filter(Group.subject.in_(value))
                    criteria = f"Subjects with id's: {value}"
                else:
                    # Return the group given a criteria
                    query = Group.query.filter(filter_map[key] == value)
                    criteria = f"{key} = {value}"

            groups = query.all()

            message = f"{len(groups)} Group/s found, filter: {criteria}"

    except Exception as e:
        logging.error(
            f'{color(1,"Couldnt get groups")} ❌: {e} {traceback.format_exc().splitlines()[-3]}')
        groups = None

    return [getGroup(group.id, 2) for group in cleanGroupQuery(groups)] if groups else None, message


