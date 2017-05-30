import json

def getJsonExample():
    with open('JSONexample1.json', 'r') as f:
        return json.load(f)

def getRows(llistaClasses):
    llistaHores = []
    for classe in llistaClasses:
        llistaHores.append(classe['startHour'][0]*60 + classe['startHour'][1])
        llistaHores.append(classe['endHour'][0]*60 + classe['endHour'][1])
    minutMinim = min(llistaHores)
    for classe in llistaClasses:
        classe['startRow'] = (classe['startHour'][0]*60 + classe['startHour'][1] - minutMinim)/30
        classe['endRow'] = (classe['endHour'][0]*60 + classe['endHour'][1] - minutMinim)/30
    return llistaClasses

def convertJSON(JSONfile):
    
    llistaClasses = []
    classe = {}
    dies = {u'monday':1, u'tuesday':2, u'wednesday':3, u'thursday': 4, u'friday': 5}
    
    llistaAssignatures = JSONfile['subjects']
    
    #Creacio dun diccionari pels colors
    llistaNoms = []
    for assignatura in llistaAssignatures:
        llistaNoms.append(assignatura['name'])
    llistaColors = []
    for i in range(0,len(llistaNoms)):
        llistaColors.append('c'+str(i))
    diccionariColors = dict(zip(llistaNoms, llistaColors))
    
    #identificador de una classe concreta
    identificador = 0 
    
    for assignatura in llistaAssignatures:
        diccionariGrups = assignatura['group']
        for numeroGrup, classesDelGrup in diccionariGrups.iteritems():
            for sessio in classesDelGrup:
                
                #Nom de la classe
                classe['name'] = assignatura['name']
                
                #Dia de la classe
                classe['day'] = sessio['day']
                classe['dayNumber'] = dies[sessio['day']]
                
                #Hora de la classe
                classe['startHour'] = [int(sessio['startHour'].split(':')[0]),int(sessio['startHour'].split(':')[1])]
                classe['endHour'] = [int(sessio['endHour'].split(':')[0]),int(sessio['endHour'].split(':')[1])]
                
                classe['startHourString'] = sessio['startHour'][0:5]
                classe['endHourString'] = sessio['endHour'][0:5]
                
                #COLOR DE LA CLASSE
                classe['color'] = diccionariColors[classe['name']]
                
                #EXTRA
                try:
                    classe['extra'] = sessio['extra']
                except KeyError:
                    pass
                
                #ALTRES
                classe['classroom'] = sessio['classroom']
                classe['grup'] = str(numeroGrup)
                classe['profe'] = 'Marc Garcia'
                classe['emailProfe'] = 'marc.garcia@gmail.com'
                classe['codi'] = assignatura['code']
                classe['id'] = identificador
                identificador += 1
                
                llistaClasses.append(classe.copy())
    
    #Calcular ROWS
    llistaClasses = getRows(llistaClasses)
    #print llistaClasses
    return llistaClasses

'''
JSONfile = getJsonExample()
    
#Obtinc una llista de totes les classes i amb les seves caracteristiques
llistaClasses = convertJSON(JSONfile)
print llistaClasses

#Calculate necessary timetable rows
filesNecessaries = getNecessaryRows(llistaClasses)
'''