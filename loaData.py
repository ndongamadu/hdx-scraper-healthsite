import requests
import json
import yaml

#prend un objet json et l'ecrit dans le dossier data, nom = fileName.geojson
def writeData(data,fileName):
    with open('data/'+fileName+'.geojson','w') as f:
            json.dump(data,f)


#recupere depuis l\API de healthsites une donnee se touvant sur pageNum
def getDataByPage(pageNum,url):
    parametres = {'page':pageNum,'format':'geojson'}
    data = []
    try:
        response = requests.get(url,params=parametres)
        data = json.loads(response.text)

    except Exception as e:
        print(e)
    return data

#recupere depuis des coord lat,long,min,max
def getBboxData(left,bottom,rigth,top,url):
    parametres ={'extent':str(left)+','+str(rigth)+','+str(top)+','+str(bottom),'format':'geojson'}
    data=[]
    try:
        response = requests.get(url,params=parametres)
        data = json.loads(response.text)
    except Exception as e:
        print(e)

    return data

def getDataByLoc(loc, url):
    parametres = {'extent':loc,'format':'geojson'}
    data=[]
    try:
        response = requests.get(url,params=parametres)
        data = json.loads(response.text)
    except Exception as e:
        print(e)

    return data

def getAllHealthSitePageData(lien):
    pn = {}
    allData = []

    with open('config/pagenumber.json') as d:
        pn = json.load(d)

    pageNumber = pn['hsPageNumber']

    with open('data/healthsites.geojson') as ad:
        allData = json.load(ad)

    if pageNumber == 0:
        allData = {"type": "FeatureCollection", "features": []}
        nbPage = 1
        dataPage = getDataByPage(1,lien)
        while dataPage['features']!= []:
            print('<---page numero %s' %nbPage)
            for dt in dataPage['features']:
                allData['features'].append(dt)
            nbPage +=1
            dataPage = getDataByPage(nbPage,lien)

        pageNumber = nbPage+1

    else:
        dataPageElse = getDataByPage(pageNumber,lien)
        while dataPageElse['features'] != []:
            for dt in dataPageElse['features']:
                allData['features'].append(dt)
            pageNumber+=1
            dataPageElse = getDataByPage(pageNumber,lien)


    #ecriture
    pn['hsPageNumber'] = pageNumber
    with open('config/pagenumber.json','w') as f:
        json.dump(pn,f)

    with open('data/healthsites.geojson','w') as fd:
        json.dump(allData,fd)

    writeData(allData,"healthfacilities")
    print('------ done ----')
