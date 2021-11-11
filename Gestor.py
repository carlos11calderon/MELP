
import mysql.connector
import json
import math, statistics
from werkzeug.wrappers import request


class Gestor:
    def __init__(self):#connection of the python with mysql database
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

    ## insert a new register in the data base restaurants
    def InsertRegister(self, iid, rating, name, site, email, phone, street, city, state, lat, lng ):
        insert = "INSERT INTO restaurants(id, rating, name, site, email, phone, street, city, state, lat, lng) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(iid, rating, name, site, email, phone, street, city, state, lat, lng)
        self.midb.execute(insert)
        self.connection.commit()#save the changes in the database
        
    def updateRegister(self, id,nameN, emailN, phoneN):# update register in the data base in the fields name, email, phone
        update1 = "UPDATE restaurants SET name='{}' WHERE id='{}'".format(nameN, id)
        update2 = "UPDATE restaurants SET email='{}' WHERE id='{}'".format(emailN, id)
        update3 = "UPDATE restaurants SET phone='{}' WHERE id='{}'".format(phoneN, id)
        self.midb.execute(update1)
        self.midb.execute(update2)
        self.midb.execute(update3)
        self.connection.commit()

    def DeleteRegister(self, id):# function that delete register in the data base
        delete = "DELETE FROM restaurants WHERE id='{}'".format(id)
        self.midb.execute(delete)
        self.connection.commit()

    def Alredy(self, lat1, lng1, radius):
        listaR=[]
        radius= float(radius)#parse to float
        lati = "SELECT lat FROM restaurants"#consulta
        self.midb.execute(lati)
        lats = self.midb.fetchall()
        longi = "SELECT lng FROM restaurants"#consulta
        self.midb.execute(longi)
        longs = self.midb.fetchall()
        i=0
        while(i<len(lats)):#ciclo para recorrer todos los registros
            lat2=lats[i]
            lat2 = lat2[0]
            lng2=longs[i]
            lng2= lng2[0]
            #calculamos la distancia 
            distance = round(self.Calculos(float(lat1), float(lng1), float(lat2),float(lng2)),2)
            if distance<=radius:#determinamos si pertenece al circulo
                rating = self.GetRating(lat2,lng2)
                if rating is not None:#agregamos a la lista rating
                    listaR.append(rating)
            i+=1
        if len(listaR)!=0:
            count = len(listaR)
            ratingProm = round((sum(listaR)/count),2)#round the prom to 2 decimal
            ratingdesv = round(statistics.pstdev(listaR),2)#redondeo la desviacion a 2 decimales
            resultado='{"Count":"'+str(count)+'", "avg":"'+str(ratingProm)+'", "std":"'+str(ratingdesv)+'"}'
            return resultado
        return '{"No exist restaurants alrady, try with other radius"}'
        
    ##in this function, we calculate the distance from center to restaurant     
    def Calculos(self,lat1, lng1, lat2,lng2 ):
        ## is the coordinates are equals, return 0 in distance
        if lat1 == lat2 and lng1 == lng2:
            return 0
        else:
            a = math.sin(lat1)*math.sin(lat2)
            b = math.cos(lat1)*math.cos(lat2)*math.cos(lng2 - lng1)
            D = math.acos(a + b)
            distance = 111.18*math.degrees(D)*1000
            return distance
    # get rating with parameters of coordinate that meet inside radius
    def GetRating(self, lat2,lng2):
        Orating = "SELECT rating FROM restaurants WHERE lat LIKE '{}' AND lng LIKE '{}'".format(lat2,lng2)
        self.midb.execute(Orating)
        rating = self.midb.fetchall()
        
        if len(rating)!=0:
            rating = rating[0]#get firts tupla
            rating = rating[0]#get first data of the tupla
            return int(rating)# return the rating type int
        else: 
            return None