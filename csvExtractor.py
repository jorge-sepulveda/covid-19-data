import csv
import pandas as pd
import json

def extractCSV():
    print('extracting the CSV')
    fields = []
    rows = []
    affectedCounties = []
    affectedCountyData = []
    with open('us-counties.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)
        for row in reversed(list(csvreader)):
            rows.append(row) 
        # get total number of rows 
        print("Total no. of rows: %d"%(csvreader.line_num))
    #print('Field names are:' + ', '.join(field for field in fields))
    # parsing each column of a row 
    for row in rows: 
        if row[3] not in affectedCounties:
            affectedCounties.append(row[3])
            affectedCountyData.append([row[1],row[2],row[3],row[4],row[5]])
    return affectedCountyData

def convertToJson(affectedCountyData):
    print('converting CSV to JSON')
    affectedCountiesJ = {}
    for countyData in affectedCountyData:
        affectedCountiesJ[str(countyData[2])] = {}
        affectedCountiesJ[str(countyData[2])]['county'] = countyData[0]
        affectedCountiesJ[str(countyData[2])]['state'] = countyData[1]
        affectedCountiesJ[str(countyData[2])]['fips'] = countyData[2]
        affectedCountiesJ[str(countyData[2])]['cases'] = countyData[3]
        affectedCountiesJ[str(countyData[2])]['deaths'] = countyData[4]
    return affectedCountiesJ

def mergeData(affectedCountiesJ):
    print('merging da data')
    counties = {}
    with open('counties.json', 'r') as file:
        counties = json.load(file)
        print(len(counties['features']))
    for i in range(len(counties['features'])):
        try:
            fipsCode = counties['features'][i]['properties']['STATE'] + counties['features'][i]['properties']['COUNTY']
            counties['features'][i]['properties']['cases'] = int(affectedCountiesJ[fipsCode]['cases'])
            counties['features'][i]['properties']['deaths'] = int(affectedCountiesJ[fipsCode]['deaths'])
            #print(counties['features'][i]['properties'])
        except Exception:
            counties['features'][i]['properties']['cases']=0
            counties['features'][i]['properties']['deaths']=0
            #print(str(counties['features'][i]['properties']) + "zeroed")
    return counties

def saveFiles(newCountyData, affectedCounties):
    print('Saving Files')
    with open('countyData.json', 'w') as f:
        json.dump(affectedCounties, f, indent=2)

    with open('counties-with-cases.json', 'w') as f:
        json.dump(newCountyData, f, separators=(',', ':'))

countyArrays = extractCSV()
affectedCountyJson = convertToJson(countyArrays)
updatedCountyData = mergeData(affectedCountyJson)
saveFiles(updatedCountyData, affectedCountyJson)