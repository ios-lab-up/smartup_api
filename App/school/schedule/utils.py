from school import db
from school.tools.utils import *
from school.tools.utils import color
from school.models import Group, Schedule, Classroom, Subject, Teacher
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
                    day=daysHours[i].split()[0], # extract day from string using split
                    startTime=datetime.strptime(daysHours[i].split()[1], '%I:%M%p').strftime('%H:%M'), # extract start time from string and convert to 24-hour format
                    endTime=datetime.strptime(daysHours[i].split()[3], '%I:%M%p').strftime('%H:%M'), # extract end time from string and convert to 24-hour format
                    classroomID=classrooms[i]
                )

                db.session.add(schedule)
                db.session.commit()

                createScheduleGroupRelation(group, schedule)

        else:
            raise ValueError(
                f'{color(1,"Cannot create schedule: Does not contain timedate objs")} ❌'
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



def getSchedule(Schedule: int) -> Schedule:
    '''Returns a object of type schedule given an id'''
    try:
        schedule = Schedule.query.filter_by(id=Schedule.id).first().toDict()
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

 
def create_compatible_schedules(groups: list[dict[str:Group]])-> list[list[dict[str:Group]]]:
    '''
    Returns a list of lists containing groups whose schedules don't overlap given a list of groups
    '''

    compatible_schedules = []
    seen_subjects = set()

    # Iterate over each group
    for schedule_1 in range(len(groups)):
        current_group = groups[schedule_1]
        current_subject = current_group['subject']

        if current_subject in seen_subjects:
            continue

        current_compatible_group = [current_group]
        seen_subjects.add(current_subject)

        # Preprocess the schedules of the current group
        current_group_schedules = preprocess_schedules(current_group['schedules'])

        # Iterate over each other group
        for schedule_2 in range(schedule_1 + 1, len(groups)):
            other_group = groups[schedule_2]
            other_subject = other_group['subject']

            if other_subject in seen_subjects:
                continue

            # Check if the schedules of the two groups overlap
            if not schedules_overlap(current_group_schedules, other_group['schedules']):
                current_compatible_group.append(other_group)
                seen_subjects.add(other_subject)

        # Add the compatible group to the list
        if len(current_compatible_group) > 1:
            compatible_schedules.append(current_compatible_group)

    return compatible_schedules


def preprocess_schedules(schedules: dict[str:Group]) -> list[dict[str:Group]]:
    '''
    Preprocesses the schedules to optimize schedule comparison,
    in order to avoid unnecesary iterations
    '''

    # Create an empty dictionary to store the preprocessed schedule data
    schedule_data = {}

    # Iterate over each schedule in the input dictionary
    for schedule in schedules:
        # Extract the relevant attributes from the schedule
        day = schedule['day']
        start_time = schedule['startTime']
        end_time = schedule['endTime']

        # If the day is not already a key in the schedule_data dictionary, add it
        if day not in schedule_data:
            schedule_data[day] = []

        # Append the schedule interval (start_time, end_time) to the corresponding day
        schedule_data[day].append((start_time, end_time))

    # Sort the schedule intervals for each day based on the start time
    for day in schedule_data:
        schedule_data[day].sort(key=lambda x: x[0])

    # Return the preprocessed schedule data
    return schedule_data


def schedules_overlap(group_1_schedules:dict[str:Group], group_2_schedules:dict[str:Group]) -> bool:
    '''
    Returns True if the schedules of group_1 and group_2 overlap, False otherwise
    '''

    #Iterate over each day in group_1_schedules
    for day in group_1_schedules:
        # Check if the day is present in group_2_schedules
        if day in group_2_schedules:
            # Get the schedule intervals for the current day in both groups
            group_1_intervals = group_1_schedules[day]
            group_2_intervals = group_2_schedules[day]

            # Iterate over each interval in group_1_intervals
            for interval_1 in group_1_intervals:
                # Iterate over each interval in group_2_intervals
                for interval_2 in group_2_intervals:
                    # Check if the intervals overlap
                    if interval_1[0] <= interval_2[1] and interval_1[1] >= interval_2[0]:
                        return True

    # If no overlap was found, return False
    return False
