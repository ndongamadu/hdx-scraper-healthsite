import requests
import json


#prend un objet json et l'ecrit dans le dossier data, nom = fileName.geojson
def writeData(data,fileName):
    try:
        with open('data/'+fileName+'.geojson','w') as f:
            json.dump(data,f)
    except Exception as e:
        print(e)

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
#Dakar extent : westlimit=-17.557354; southlimit=14.644711; eastlimit=-17.103138; northlimit=14.890378
def getDataFromBbox(left,rigth,top,bottom,url):
    parametres ={'extent':str(left)+','+str(rigth)+','+str(top)+','+str(bottom),'format':'geojson'}
    data=[]
    try:
        response = requests.get(url,params=parametres)
        data = json.loads(response.text)
    except Exception as e:
        print(e)

    return data
