import json, math

def getJsonExample():
    with open('static/json/edu.json', 'r') as f:
        return json.load(f)

def getRows(llistaClasses):
    llistaHores = []
    for classe in llistaClasses:
        llistaHores.append(classe['startHour'][0]*60 + classe['startHour'][1])
        llistaHores.append(classe['endHour'][0]*60 + classe['endHour'][1])
    minutMinim = min(llistaHores)
    for classe in llistaClasses:
        classe['startRow'] = (classe['startHour'][0]*60 + classe['startHour'][1] - minutMinim)/30.
        classe['endRow'] = (classe['endHour'][0]*60 + classe['endHour'][1] - minutMinim)/30.
    return llistaClasses

def filesNecessaries(llistaClasses):
    filaMax = 0
    for classe in llistaClasses:
        if classe['endRow'] > filaMax:
            filaMax = classe['endRow']
    return int(math.ceil(filaMax))

def trobarCanal(canals):
    for i in range(0,len(canals)):
        if canals[i] == 0:
            return i+1
    return False

def insertarSolapaments(llistaClasses):
    files = filesNecessaries(llistaClasses)
    for day in range(1,6):
        canalsActius = [0,0,0,0,0]
        for fila in range(0, files+1):
            for classe in llistaClasses:
                if classe['dayNumber'] == day:
                    if classe['endRow']-1 == fila:
                        canalsActius[classe['canal']-1] = 0
                    elif classe['startRow'] == fila :
                        canalAssignat = trobarCanal(canalsActius)
                        classe['canal'] = canalAssignat
                        canalsActius[canalAssignat-1] = 1
    for i in range(0, len(llistaClasses)):
        for j in range(0, len(llistaClasses)):
            if i != j:
                if llistaClasses[i]['dayNumber'] == llistaClasses[j]['dayNumber']:
                    if llistaClasses[i]['startRow'] >= llistaClasses[j]['startRow'] and llistaClasses[i]['startRow'] < llistaClasses[j]['endRow']:
                        paralel = max(llistaClasses[i]['canal'], llistaClasses[j]['canal'])
                        if llistaClasses[i]['paralel'] < paralel:
                            llistaClasses[i]['paralel'] = paralel
                        if llistaClasses[j]['paralel'] < paralel:
                            llistaClasses[j]['paralel'] = paralel
    return llistaClasses

def convertJSON(jsonFile):
    
    llistaClasses = []
    classe = {}
    dies = {u'monday':1, u'tuesday':2, u'wednesday':3, u'thursday': 4, u'friday': 5}
    
    llistaAssignatures = jsonFile['subjects']
    
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
                
                #ALTRES
                classe['classroom'] = sessio['classroom']
                classe['grup'] = str(numeroGrup)
                classe['profe'] = 'Marc Garcia'
                classe['emailProfe'] = 'marc.garcia@gmail.com'
                classe['codi'] = assignatura['code']
                classe['id'] = identificador
                classe['lan'] = 'ENG'
                identificador += 1
                
                #inicialitzacio de solapament
                classe['canal'] = 1
                classe['paralel'] = 1
                
                #EXTRA i afegir
                try:
                    classe['extra'] = sessio['extra']
                    if classe['extra'][0] == '(':
                        llistaClasses.append(classe.copy())
                except KeyError:
                    classe['extra'] = ''
                    llistaClasses.append(classe.copy())
    
    #Calcular ROWS
    llistaClasses = getRows(llistaClasses)
    
	#calcular solapaments
    llistaClasses = insertarSolapaments(llistaClasses)
    return llistaClasses