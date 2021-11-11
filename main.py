from flask import *
from flask_cors import CORS
from Gestor import Gestor

gestor=Gestor()

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return 'SERVER IS WORKING!!!!'

@app.route('/ViewData', methods=['GET'])#view data method READ
def getData():
    return gestor.ViewRegisters()

@app.route('/CreateRegister', methods=['POST'])#method CREATE
def insertRegister():
    data = request.json
    gestor.InsertRegister(data['id'], data['rating'], data['name'], data['site'], data['email'], data['phone'], data['street'], data['city'], data['state'], data['lat'], data['lng'])
    return '{"Estado":"Registro creado"}'

@app.route('/UpdateRegister/<id>', methods=['PUT'])#method UPDATE
def UpdateRegister(id):
    data = request.json
    print(data)
    gestor.updateRegister(id,data['name'],data['email'], data['phone'])
    return '{"Estado":"Registro actualizado"}'

@app.route('/Delete', methods=['DELETE'])#method DELETE
def DeleteRegister():
    data = request.json
    gestor.DeleteRegister(data['id'])
    return '{"Estado":"Registro Eliminado"}'

@app.route('/Alredy/statistics', methods=['GET'])
def Alredy():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    radius = request.args.get('radius')
    resultado=gestor.Alredy(latitude,longitude,radius)
    return resultado
    

#Iniciamos el servidor

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True )
        