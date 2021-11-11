from flask import *
from flask_cors import CORS
from Gestor import Gestor
import mysql.connector

gestor=Gestor()

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return 'SERVER IS WORKING!!!!'

@app.route('/MostrarDatos', methods=['GET'])
def getData():
    return gestor.ViewRegisters()

@app.route('/CreateRegister', methods=['POST'])
def insertRegister():
    data = request.json
    gestor.InsertRegister(data['id'], data['rating'], data['name'], data['site'], data['email'], data['phone'], data['street'], data['city'], data['state'], data['lat'], data['lng'])
    return '{"Estado":"Registro creado"}'

@app.route('/UpdateRegister/<id>', methods=['PUT'])
def UpdateRegister(id):
    data = request.json
    print(data)
    gestor.updateRegister(id,data['name'],data['email'], data['phone'])
    return '{"Estado":"Registro actualizado"}'

@app.route('/Delete', methods=['DELETE'])
def DeleteRegister():
    data = request.json
    gestor.DeleteRegister(data['id'])
    return '{"Estado":"Registro Eliminado"}'

@app.route('/Alredy/<latitud>/<longitud>/<radius>', methods=['GET'])
def Alredy(latitud, longitud, radius):
    data = request.json
    resultado=gestor.Alredy(latitud,longitud,radius)
    return resultado
    

#Iniciamos el servidor

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True )
        