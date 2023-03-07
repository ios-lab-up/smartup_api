from school.models import *
from school import db


RelationGroupSchedule = db.Table('RelationGroupSchedule',
                                 db.Column('groupId', db.Integer,
                                           db.ForeignKey('Group.id')),
                                 db.Column('scheduleID', db.Integer,
                                           db.ForeignKey('Schedule.id')),
                                 )


RelationStudentSubjectTable = db.Table('RelationStudentSubjectTable',
                                       db.Column('studentId', db.Integer,
                                                 db.ForeignKey('Student.id'), ),
                                       db.Column('subjectId', db.Integer, db.ForeignKey('Subject.id')),)
