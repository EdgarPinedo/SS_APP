import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from similarity import buscar

cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

from flask import *

app = Flask(__name__)

#index page

@app.route('/')
def index():
    materias = db.collection('Materias').get()
    list = []
    for materia in materias:
        list.append(materia.to_dict())
    return render_template('index.html', mats = list)

@app.route('/busqueda', methods = ['POST'])
def busqueda():
    if request.method == 'POST':
        materias = db.collection('Materias').get()
        list = []
        stringBusqueda = request.form['search']
        for materia in materias:
            strings = [materia.to_dict()['tittle'], stringBusqueda]
            similarity = buscar(strings)
            if(similarity > 0.36):
                list.append(materia.to_dict())
    return render_template('index.html', mats = list)


# Agregar page

@app.route('/new')
def new():
    return render_template('agregar.html')

@app.route('/agregarmateria', methods = ['POST'])
def agregarMateria():    
    if request.method == 'POST':
        id = request.form['id']
        title = request.form['tittle']
        description = request.form['description']
        data = {'id':id, 'tittle':title, 'description':description}
        db.collection('Materias').document(id).set(data)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug = True)        