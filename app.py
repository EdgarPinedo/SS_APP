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
        categoria = request.form['categoria']
        description = request.form['description']
        competenciaU = request.form['competenciaU']
        competenciaG = request.form['competenciaG']
        competenciaP = request.form['competenciaP']
        contenido = request.form['contenido']
        data = {'id':id, 'title':title, 'categoria':categoria, 'description':description, 
                'competenciaU':competenciaU, 'competenciaG':competenciaG, 'competenciaP':competenciaP, 'contenido':contenido}
        db.collection('Materias INCO').document(id).set(data)
    return redirect(url_for('index'))


# Ver detalles de materia

@app.route('/detalles/<id>')
def show(id):
    materia = db.collection('Materias').where("id", "==", id).get()[0].to_dict()
    return render_template('show.html', mat = materia)

if __name__ == '__main__':
    app.run(debug = True)        