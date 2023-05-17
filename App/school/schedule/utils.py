from school import db
from school.tools.utils import *
from school.tools.utils import color
from school.models import Group, User, Schedule, Classroom, Days, Hours
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

                # schedule = Schedule(
                #     # Dia: str
                #     day=daysHours[i][0:str(daysHours[i]).index(' ')],
                #     startTime=f"{int(daysHours[i][daysHours[i].index(' ') + 1:daysHours[i].index(':')]) + 12 if int(daysHours[i][daysHours[i].index(' ') + 1:daysHours[i].index(':')]) != 12 else int(daysHours[i][daysHours[i].index(' ') + 1:daysHours[i].index(':')])}:" \
                #     f"{daysHours[i][daysHours[i].index(' ') + 1:daysHours[i].index('-') - 1][-6:-4]}:00" \
                #     if 'p' in daysHours[i][daysHours[i].index(' ') + 1:daysHours[i].index('-') - 1] \

                #     else f"{daysHours[i][daysHours[i].index(' ') + 1:daysHours[i].index(':')]}:" \
                #     f"{daysHours[i][daysHours[i].index(' ') + 1:daysHours[i].index('-') - 1][-6:-4]}:00",  # Hora de inicio: datetime

                #     endTime=f"{int(daysHours[i][daysHours[i].index('-') + 1:daysHours[i].rindex(':')]) + 12 if int(daysHours[i][daysHours[i].index('-') + 1:daysHours[i].rindex(':')]) != 12 else daysHours[i][daysHours[i].index('-') + 1:daysHours[i].rindex(':')]}:" \
                #     f"{daysHours[i][daysHours[i].index('-') + 1:][-6:-4]}:00" \
                #     if 'p' in daysHours[i][daysHours[i].index('-') + 1:] \
                #     else f"{int(daysHours[i][daysHours[i].index('-') + 1:daysHours[i].rindex(':')])}:" \
                #     f"{daysHours[i][daysHours[i].index('-') + 1:][-6:-4]}:00",
                #     classroomID=classrooms[i]
                # )
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





def schedulesOverlap(group_1: Group, group_2) -> bool:
    '''
    Returns true in case they overlap in time and day else it returns false
    it takes into consideration the following criteria:
    - If the startTime or endTime of both groups somehow overlaps = True
    - If the startTime or endTime of one group is in between the startTime and endTime of the other group = True

    This criteria is applied for each day of the group, if its not achieved return True, else False
    '''
    try:
        if group_1 and group_2:
            for schedule_1 in group_1.schedule:
                for schedule_2 in group_2.schedule:
                    if schedule_1.day == schedule_2.day:
                        if schedule_1.startTime <= schedule_2.startTime <= schedule_1.endTime or schedule_1.startTime <= schedule_2.endTime <= schedule_1.endTime:
                            return True
                        elif schedule_2.startTime <= schedule_1.startTime <= schedule_2.endTime or schedule_2.startTime <= schedule_1.endTime <= schedule_2.endTime:
                            return True
                        else:
                            return False
        else:
            raise ValueError(
                f'{color(1,"Cannot compare schedules: Does not contain timedate objs")} ❌'
            )        
                    
       
    except Exception as e:
        logging.critical(
            f'{color(5,"Schedule comparison failed")} ❌: {e}\n{traceback.format_exc().splitlines()[-3]}')
        return False
    

def createCompatibleSchedules(groups: list[Group]) -> list[list[Group]]:
    '''
    Returns a list of groups that are compatible with each other using backtracking
    '''
