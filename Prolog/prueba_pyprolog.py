from pyswip import Prolog

prolog = Prolog()

prolog.consult('/home/ricardo/Dropbox/SisInt/ProyectoFinal/PC/Controlador/prolog/prueba.pl')

objetos = []
for objeto in list(prolog.query('ubicacion(Objeto,sala)')):
	objetos.append(objeto['Objeto'])

print(list(prolog.query('persona(Ubicacion)'))[0]['Ubicacion'])
print(objetos)
