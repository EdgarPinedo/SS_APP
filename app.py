import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from similarity import buscar
import html

cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

from flask import *

app = Flask(__name__)

#index page

@app.route('/')
def index():
    materias = db.collection('Materias INCO').get()
    list = []
    for materia in materias:
        list.append(materia.to_dict())
    return render_template('index.html', mats = list, _index = "inco")

@app.route('/INNI')
def inni():
    materias = db.collection('Materias').get()
    list = []
    for materia in materias:
        list.append(materia.to_dict())
    return render_template('index.html', mats = list, _index = "inni")


#buscar materias

@app.route('/busqueda/<index>', methods = ['POST'])
def busqueda(index):
    if request.method == 'POST':
        list = []
        
        if index == "inco":
            materias = db.collection('Materias INCO').get()
        elif index == "inni":
            materias = db.collection('Materias').get()

        stringBusqueda = request.form['search']
        for materia in materias:
            strings = [materia.to_dict()['title'], stringBusqueda]
            similarity = buscar(strings)
            if(similarity > 0.36):
                list.append(materia.to_dict())

    return render_template('index.html', mats = list, _index = index)


# Agregar materia

@app.route('/new')
def new():
    return render_template('agregar.html')

@app.route('/agregarmateria', methods = ['POST'])
def agregarMateria():    
    if request.method == 'POST':
        id = request.form['id']
        title = request.form['title']
        categoria = request.form['categoria']
        description = request.form['description']
        competenciaU = request.form['competenciaU']
        competenciaG = request.form['competenciaG']
        competenciaP = request.form['competenciaP']
        contenido = request.form['contenido']
        carrera = request.form['index']
        data = {'id':id, 'title':title, 'categoria':categoria, 'description':description, 
                'competenciaU':competenciaU, 'competenciaG':competenciaG, 'competenciaP':competenciaP, 'contenido':contenido}
        
        if carrera == "INCO":
            db.collection('Materias INCO').document(id).set(data)
            return redirect(url_for('index'))
        else:
            db.collection('Materias').document(id).set(data)
            return redirect(url_for('/INNI'))
    


# Ver detalles de materia

@app.route('/detalles/<carrera>/<id>')
def show(carrera, id):
    if carrera == "inco":
        materia = db.collection('Materias INCO').where("id", "==", id).get()[0].to_dict()
    elif carrera == "inni":
        materia = db.collection('Materias').where("id", "==", id).get()[0].to_dict()
    return render_template('show.html', mat = materia)

# Eliminar materia

@app.route('/eliminarmateria', methods = ['GET', 'DELETE'])
def eliminarMateria():
    try:
        if request.method == 'GET':
            id = request.args.get('id')
            carrera = request.args.get('carrera')
            if carrera == "INCO":
                db.collection('Materias INCO').document(id).delete()
            else:
                db.collection('Materias').document(id).delete()
        return redirect(url_for('index'))
    except Exception as e:
        return f'Error: {e}'
        

if __name__ == '__main__':
    app.run(debug = True)