#healthsites API documentation https://github.com/healthsites/healthsites/wiki/API
#https://healthsites.io/api/v1/healthsites/search?search_type=facility&name=benin&format=json

import logging
from hdx.data.dataset import Dataset
from hdx.data.resource import Resource
import requests
from slugify import slugify
import json
import time
import csv
import os
import shutil
import subprocess

logger = logging.getLogger(__name__)

## v2 ## https://healthsites.io/api/v1/healthsites/search?search_type=placename&format=geojson$name=

# create the data folder 

def getCountryHealthSites(configuration,countryName):
    print('<------- Generating %s dataset -------->' %countryName)

    url = configuration.read()['base_url']+configuration.read()['api_version']+configuration.read()['api_name']+"search?search_type=placename&format=geojson"
    countryData = {"type": "FeatureCollection", "features": []}
    try:
        with open('data/'+countryName+'.geojson','r') as f:
            countryData = json.load(f)
    except Exception as e:
        pass
    newData = {"type": "FeatureCollection", "features": []}
    parameters = {'name':countryName,'page':0}
    nbPage = 1
    #iterate on page number
    #get data by page and return newData with all the data
    while 1:
        parameters['page'] = nbPage
        response = requests.get(url,params=parameters)
        data = json.loads(response.text)
        if(data['features']==[]):
            break
        else:
            for dt in data['features']:
                newData['features'].append(dt)
            nbPage+=1
    #write if newData different from the potential existing file (update)
    if(len(newData['features'])> len(countryData['features'])):
        #write the file to use to create de shp
        with open(configuration.read()['data_folder']+'healthsites.geojson','w') as f:
            json.dump(newData,f)
        #write the geojson with the country name
        with open(configuration.read()['data_folder']+countryName+'.geojson','w') as f2:
            json.dump(newData,f2)
        #write to csv
        subprocess.call("./geojsonToCSV.sh",shell=True)
        #write the shp
        subprocess.call("./writeToSHP.sh",shell=True)
        #rename the shp to the country name
        if(os.path.isfile(configuration.read()['data_folder']+"shapefiles.zip")):
            shutil.move(configuration.read()['data_folder']+"shapefiles.zip", configuration.read()['data_folder']+countryName+"-shapefiles.zip")
        #rename the csv to the country name
        if(os.path.isfile(configuration.read()['data_folder']+"healthsites.csv")):
            shutil.move(configuration.read()['data_folder']+"healthsites.csv", configuration.read()['data_folder']+countryName+".csv")
        #rename the geojson to the country name
        shutil.move(configuration.read()['data_folder']+"healthsites.geojson", configuration.read()['data_folder']+countryName+".geojson")

        print("===== %s files generated ! ======" %countryName)
    else:
        #skip writing new file
        #test and create the shp if not exists
        if(os.path.isfile(configuration.read()['data_folder']+countryName+"-shapefiles.zip") == False):
            shutil.copy(configuration.read()['data_folder']+countryName+'.geojson', configuration.read()['data_folder']+"healthsites.geojson")
            subprocess.call("./writeToSHP.sh",shell=True)
            shutil.move(configuration.read()['data_folder']+"shapefiles.zip", configuration.read()['data_folder']+countryName+"-shapefiles.zip")

        #test and create the csv if not exits
        if(os.path.isfile(configuration.read()['data_folder']+countryName+".csv")== False):
            shutil.copy(configuration.read()['data_folder']+countryName+'.geojson', configuration.read()['data_folder']+"healthsites.geojson")
            subprocess.call("./geojsonToCSV.sh",shell=True)
            shutil.move(configuration.read()['data_folder']+"healthsites.csv", configuration.read()['data_folder']+countryName+".csv")

        print('<=========== file exists ! =========>')

def generate_dataset(configuration,countryName):
    showedName = countryName
    if(countryName=="Ivory Coast"):
        showedName="Cote d'Ivoire"
    name = countryName+'-healthsites'
    title = countryName+'-healthsites'
    slugified_name = slugify(name).lower()
    # dataset = Dataset(configuration, {
    # })
    dataset = Dataset({
        'name': slugified_name,
        'title': title,
    })
    # dataset['name'] = slugified_name
    # dataset['title'] = title
    #generating the datasets
    getCountryHealthSites(configuration,countryName)
    # geojson resource
    if(os.path.isfile(configuration.read()['data_folder']+countryName+'.geojson')):
        rName = countryName+'-healthsites-geojson'
        geojsonResource = Resource()
        geojsonResource['name'] = rName
        geojsonResource['format'] = 'geojson'
        geojsonResource['url'] = configuration.read()['base_url']
        geojsonResource['description'] = countryName+' healthsites geojson'
        # geojsonResource.set_file_to_upload(configuration.read()['data_folder']+countryName+'.geojson')
        geojsonResource.set_file_to_upload('data/'+countryName+'.geojson')

        geojsonResource.check_required_fields(['group','package_id'])
        dataset.add_update_resource(geojsonResource)
    #csv resource
    if(os.path.isfile(configuration.read()['data_folder']+countryName+'.csv')):
        resource_csv = Resource()
        resource_csv['name'] = countryName+'-healthsites-csv'
        resource_csv['description'] = countryName+' healthsites csv'
        resource_csv['format'] = 'csv'
        # resource_csv.set_file_to_upload(configuration.read()['data_folder']+countryName+'.csv')
        resource_csv.set_file_to_upload('data/'+countryName+'.csv')

        resource_csv.check_required_fields(['group','package_id'])
        dataset.add_update_resource(resource_csv)
    # shp resource
    if(os.path.isfile(configuration.read()['data_folder']+countryName+"-shapefiles.zip")):
        resource_shp = Resource()
        resource_shp['name'] = countryName+'-healthsites-shp'
        resource_shp['format'] = 'zipped shapefile'
        resource_shp['description'] = countryName+' healthsites shapefiles'
        # resource_shp.set_file_to_upload(configuration.read()['data_folder']+countryName+"-shapefiles.zip")
        resource_shp.set_file_to_upload('data/'+countryName+'-shapefiles.zip')

        resource_shp.check_required_fields(['group','package_id'])
        dataset.add_update_resource(resource_shp)


    return dataset
