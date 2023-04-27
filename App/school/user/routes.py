from school.models import User
# from school.schedule.utils import getSubject, getUserSubjects
from flask import Blueprint, request, jsonify, session
from school.scrapper.utils import *

print("Importing user routes")
#Este codigo es para que no se importe el modulo de scrapper en el momento de importar el modulo de user routes 
#el modulo de scrapper importa el modulo de user routes y viceversa, por lo que se crea un ciclo infinito
user = Blueprint('user', __name__)

