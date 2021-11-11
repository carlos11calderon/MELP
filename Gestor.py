
from logging import NullHandler
from os import stat
import re
import mysql.connector
import json
import math, statistics
from werkzeug.wrappers import request





class Gestor:
    def __init__(self):
        self.connection = mysql.connector.connect(user='root', password='Augusto11cal', host='localhost', database='melp', port='3306')
        self.midb = self.connection.cursor() 
    
    
    #Devuelve registros de la tabla sql en formato json - return registers of the table sql in json format 
    def ViewRegisters(self):
        view = 'SELECT * FROM restaurants'
        self.midb.execute(view)    
        field_names = [i[0] for i in self.midb.description]
        restaurants = self.midb.fetchall()
        json_data=[]
        for i in restaurants:
           json_data.append(dict(zip(field_names, i)))
        return json.dumps(json_data)

    
    def InsertRegister(self, iid, rating, name, site, email, phone, street, city, state, lat, lng ):
        insert = "INSERT INTO restaurants(id, rating, name, site, email, phone, street, city, state, lat, lng) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(iid, rating, name, site, email, phone, street, city, state, lat, lng)
        self.midb.execute(insert)
        self.connection.commit()
        
    def updateRegister(self, id,nameN, emailN, phoneN):
        update1 = "UPDATE restaurants SET name='{}' WHERE id='{}'".format(nameN, id)
        update2 = "UPDATE restaurants SET email='{}' WHERE id='{}'".format(emailN, id)
        update3 = "UPDATE restaurants SET phone='{}' WHERE id='{}'".format(phoneN, id)
        self.midb.execute(update1)
        self.midb.execute(update2)
        self.midb.execute(update3)
        self.connection.commit()

    def DeleteRegister(self, id):
        delete = "DELETE FROM restaurants WHERE id='{}'".format(id)
        self.midb.execute(delete)
        self.connection.commit()

    def Alredy(self, lat1, lng1, radius):
        listaR=[]
        radius= float(radius)
        lati = "SELECT lat FROM restaurants"
        self.midb.execute(lati)
        lats = self.midb.fetchall()
        longi = "SELECT lng FROM restaurants"
        self.midb.execute(longi)
        longs = self.midb.fetchall()
        i=0
        while(i<len(lats)):
            lat2=lats[i]
            lat2 = lat2[0]
            lng2=longs[i]
            lng2= lng2[0]
            print("latitud: "+str(lat2)+" long: "+str(lng2))
            distance = round(self.Calculos(float(lat1), float(lng1), float(lat2),float(lng2)),2)
            if distance<=radius:
                print(radius)
                print("DISTANCIA ES: "+str(distance))
                rating = self.GetRating(lat2,lng2)
                if rating is not None:
                    listaR.append(rating)
            i+=1
        if len(listaR)!=0:
            count = len(listaR)
            ratingProm = round((sum(listaR)/count),2)#redondeo el promedio a 2 decimales
            ratingdesv = round(statistics.pstdev(listaR),2)#redondeo la desviacion a 2 decimales
            resultado='{"Count":"'+str(count)+'", "avg":"'+str(ratingProm)+'", "std":"'+str(ratingdesv)+'"}'
            return resultado
        return '{"No se pudo"}'
        
    def Calculos(self,lat1, lng1, lat2,lng2 ):
        
        if lat1 == lat2 and lng1 == lng2:
            return 0
        else:
            a = math.sin(lat1)*math.sin(lat2)
            b = math.cos(lat1)*math.cos(lat2)*math.cos(lng2 - lng1)
            D = math.acos(a + b)
            distance = 111.18*math.degrees(D)*1000
            return distance
    
    def GetRating(self, lat2,lng2):
        Orating = "SELECT rating FROM restaurants WHERE lat LIKE '{}' AND lng LIKE '{}'".format(lat2,lng2)
        print(Orating)
        self.midb.execute(Orating)
        rating = self.midb.fetchall()
        if len(rating)!=0:
            rating = rating[0]#obtengo la primera tupla
            rating = rating[0]#obtengo el primer dato de la tupla
            return int(rating)# retorno el rating tipo int
        else: 
            return None