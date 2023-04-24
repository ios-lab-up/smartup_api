import os
def clear():
    input("Presiona enter para continuar...")
    os.system('cls')
def SplitNombres( nombre ):
    tokens = nombre.split(" ")
    names = []
    especial_tokens = ['da', 'de', 'di', 'do', 'del', 'la', 'las', 
    'le', 'los', 'mac', 'mc', 'van', 'von', 'y', 'i', 'san', 'santa']
    prev = ""
    for token in tokens:
        _token = token.lower()
        if _token in especial_tokens:
            prev += token + " "
        else:
            names.append(prev + token)
            prev = ""
    num_nombres = len(names)
    nombres, apellido1, apellido2 = "", "", ""
    if num_nombres == 0:
        nombres = ""
    elif num_nombres == 1:
        nombres = names[0]
    elif num_nombres == 2:
        nombres = names[0]
        apellido1 = names[1]
    elif num_nombres == 3:
        nombres = names[0]
        apellido1 = names[1]
        apellido2 = names[2]
    else:
        nombres = names[0] + " " + names[1]
        apellido1 = names[2]
        apellido2 = names[3]
    nombres = nombres.title()
    apellido1 = apellido1.title()
    apellido2 = apellido2.title()
    nombre_apellido=[nombres,(apellido1 +' '+apellido2)]
    return nombre_apellido

Pruebas= ['Javier Alejandro Rangel Murillo','Jesus Alejandro Lopez' ,'Maria del Carmen Lopez Rodriguez','Luis Cedillo Maldonado', 'Melany De la Cruz Toscano', 'Juan Esteban Mayoral Zepeda', 'Emiliano del Jesus Lopez', 'Mónica Patricia de Ávalos Mendoza', 'Gabriela de la Pava de la Torre', 'Juan Fernando Pérez del Corral', 'Valentina Laverde de la Rosa', 'Óscar de la Renta', 'Sara Teresa Sánchez del Pinar', 'Efraín de las Casas Mejía', 'Julieta Ponce de León', 'Martín Elías de los Ríos Acosta', 'Gabriela de la Pava de la Torre', 'Matías de Greiff Rincón', 'Manuela del Pino Hincapié', 'Sebastián del Campo Yepes', 'Sofía del Río Arango', 'Ana María de la Peña Posada', 'Mónica Patricia de Ávalos Mendoza']

for nombre in Pruebas:
    print(nombre)
    print(SplitNombres(nombre))
    clear()