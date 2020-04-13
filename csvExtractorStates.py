import csv
import pandas as pd
import json

def extractCSV():
    print('extracting the States CSV')
    fields = []
    rows = []
    affectedStates = []
    affectedStateData = []
    with open('us-states.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)
        for row in reversed(list(csvreader)):
            rows.append(row) 
        # get total number of rows 
        print("Total no. of rows: %d"%(csvreader.line_num))
    print('Field names are:' + ', '.join(field for field in fields))
    # parsing each column of a row 
    for row in rows: 
        if row[2] not in affectedStates:
            affectedStates.append(row[2])
            affectedStateData.append([row[1],row[2],row[3],row[4]])
    return affectedStateData

def convertToJson(affectedStateData):
    print('converting CSV to JSON')
    affectedStatesJ = {}
    for stateData in affectedStateData:
        #print(stateData)
        affectedStatesJ[str(stateData[1])] = {}
        affectedStatesJ[str(stateData[1])]['state'] = stateData[0]
        affectedStatesJ[str(stateData[1])]['fips'] = stateData[1]
        affectedStatesJ[str(stateData[1])]['cases'] = stateData[2]
        affectedStatesJ[str(stateData[1])]['deaths'] = stateData[3]
    return affectedStatesJ

def mergeData(affectedStatesJ):
    print('merging da data')
    states = {}
    with open('states.json', 'r') as file:
        states = json.load(file)
        print('should be a lil over 50')
        print(len(states['features']))
    for i in range(len(states['features'])):
        try:
            fipsCode = states['features'][i]['properties']['STATE']
            states['features'][i]['properties']['cases'] = int(affectedStatesJ[fipsCode]['cases'])
            states['features'][i]['properties']['deaths'] = int(affectedStatesJ[fipsCode]['deaths'])
            #print(counties['features'][i]['properties'])
        except Exception:
            states['features'][i]['properties']['cases']=0
            states['features'][i]['properties']['deaths']=0
            #print(str(counties['features'][i]['properties']) + "zeroed")
    return states

def saveFiles(newCountyData, affectedCounties):
    print('Saving Files')
    with open('stateData.json', 'w') as f:
        json.dump(affectedCounties, f, indent=2)

    with open('states-with-cases.json', 'w') as f:
        json.dump(newCountyData, f, separators=(',', ':'))

print('Extracting Data to States')
stateArrays = extractCSV()
affectedStateJson = convertToJson(stateArrays)
updatedStateData = mergeData(affectedStateJson)
saveFiles(updatedStateData, affectedStateJson)