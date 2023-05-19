from school.models import Group
from school.groups.utils import *
import logging
import traceback
from school.tools.utils import color


def createCompatibleSchedules(groups: dict[Group]) -> list[list[dict[Group]]]:
    '''
    Returns a list of lists containing groups whose schedules don't overlap given a list of groups
    '''

    compatible_schedules = []
    groups.sort(key=lambda group: group.get('subject'))  # Sort groups by subject
    for group in groups:
        print(group.get('subject'))
        
    # Iterate over each group
    for i in range(len(groups)):
        compatible_group = [groups[i]]
        seen_subjects = set([groups[i].get('subject')])  # Track subjects encountered
        # Iterate over each other group
        for j in range(i + 1, len(groups)):
            # Check if the schedules of the two groups overlap and the subject is not repeated
            if (
                not schedulesOverlap(groups[i], groups[j]) and
                groups[j].get('subject') not in seen_subjects
            ):
                compatible_group.append(groups[j])
                seen_subjects.add(groups[j].get('subject'))

        compatible_schedules.append(compatible_group)
    # Return the list of compatible schedules

    return compatible_schedules


def schedulesOverlap(group_1: Group, group_2: Group) -> bool:
    '''
    Returns True if the schedules of group_1 and group_2 overlap, False otherwise
    '''

    try:
        # Get the schedules of each group
        group_1_schedules = group_1.schedule
        group_2_schedules = group_2.schedule

        # Iterate over each schedule in group 1
        for schedule_1 in group_1_schedules:
            # Iterate over each schedule in group 2
            for schedule_2 in group_2_schedules:
                # Check if the days are the same
                if schedule_1['day'] == schedule_2['day']:
                    # Check if the times overlap
                    if (
                        schedule_1['startTime'] <= schedule_2['endTime'] and
                        schedule_1['endTime'] >= schedule_2['startTime']
                    ):
                        return True

        # If no overlap was found, return False
        return False

    except Exception as e:
        logging.critical(f'Schedule comparison failed: {e}')
        return False
