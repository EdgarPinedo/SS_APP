import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json

cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

### Agregar json ###

# nuevaMateria = db.collection('Materias').document('Alm. Datos')
# nuevaMateria.set({
#     'id': 'I5906',
#     'tittle': 'Almacenes de Datos',
#     'description': 'Los almacenes de datos (datawarehouse, en inglés) representan la forma de extracción e interpretación de los datos generados principalmente por las compañías para ejercer una toma de decisiones y mejorar la calidad de un servicio o producto con el objetivo de incrementar sus ventas o generar una visión futura, conforme a los datos históricos de la compañía, para expandir, producir o generar un nuevo producto. Esta materia requiere conocimientos de minería de datos para aplicar algunas técnicas de interpretación de datos y generar los resultados en forma de gráficos, generalmente, y ser presentados a la autoridad máxima de la empresa, en una forma entendible y con datos “duros” para éste pueda determinar el rumbo de la misma.'
# })

# Ya con el html usaremos este
# data = {'id':id, 'tittle':tittle, 'description':description}
# db.collection('Materias').document('Name').set(data)


### Obtener todos los json ###

# materias = db.collection('Materias').get()
# for materia in materias:
#     print(materia.to_dict())

materias = db.collection('Materias').get()
list = []
for materia in materias:
    list.append(materia.to_dict())

#jsonToString = json.dumps(materia)
#jsonload = json.loads(jsonToString)
print(list)

from flask import *

app = Flask(__name__)

@app.route('/')
def index():
    materias = db.collection('Materias').get()
    #materias = materias.to_dict()
    #print(materias)
    list = []
    for materia in materias:
        list.append(materia.to_dict())
    return render_template('index.html', mats = list)
    #return materia['id']


if __name__ == '__main__':
    app.run(debug = True)        