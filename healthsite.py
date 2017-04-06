#healthsites API documentation https://github.com/healthsites/healthsites/wiki/API
import logging
from hdx.data.dataset import Dataset
from hdx.data.resource import Resource
import requests
from slugify import slugify
import json
import time
import csv
import pandas as pd
import os
import subprocess

logger = logging.getLogger(__name__)

def writeCsv(countryName):
    print('<------ creating csv file ------->')
    with open('data/'+countryName+'.json') as jd :
        data = json.load(jd)
        pandasData = pd.DataFrame(data)
        pandasData.to_csv('data/'+countryName+'.csv')
    print('<----- csv created ----->')

def generateCountryDataset(countryName):

    print('<------- Generating %s dataset -------->' %countryName)
    urlgeojson ="https://healthsites.io/api/v1/healthsites/search?search_type=placename&format=geojson"
    urljson = "https://healthsites.io/api/v1/healthsites/search?search_type=placename&format=json"

    parametres = {'name':countryName}
    countryData = {"type": "FeatureCollection", "features": []}

    try:
        with open('data/'+countryName+'.geojson','r') as f:
            countryData = json.load(f)
    except Exception as e:
        pass

    try:
        response = requests.get(urlgeojson,params=parametres)
        responseJson = requests.get(urljson,params=parametres)
        data = json.loads(response.text)
        dataJson = json.loads(responseJson.text)
        if(len(data['features'])>len(countryData['features'])):
            with open('data/healthsites.geojson','w') as f:
                json.dump(data,f)

            with open('data/'+countryName+'.json','w') as f:
                json.dump(dataJson,f)

            # subprocess.call("./writeToSHP.sh", shell=True)
            with open('data/'+countryName+'.geojson','w') as f:
                json.dump(data,f)
            writeCsv(countryName)
            print('<------- File created in data folder --------->')

        else:
            # subprocess.call("./writeToSHP.sh", shell=True)
            print('File exists yet & there is no updates')

    except Exception as e:
        print('>---- pays non reconnu %s----<'%e)
        pass

def generate_dataset(configuration,countryName):
    name = countryName+' health facilities'
    title = countryName+' healthsites'
    slugified_name = slugify(name).lower()
    dataset = Dataset(configuration, {
    })
    dataset['name'] = slugified_name
    dataset['title'] = title

    #geojson resource
    # rName = countryName+'-healthsites-geojson'
    # resource = Resource()
    # resource['name'] = rName
    # resource['format'] = 'geojson'
    # resource['url'] = configuration['base_url']
    # resource['description'] = configuration['base_url']
    # resource['url_type'] = 'api'
    # resource['resource_type'] = 'api'

    generateCountryDataset(countryName)

    #csv resource
    resource_csv = Resource()
    resource_csv['name'] = countryName+'-healthsites-csv'
    resource_csv['description'] = countryName+' healthsites csv'
    resource_csv['format'] = 'csv'

    #shp resource
    # resource_shp = Resource()
    # resource_shp['name'] = countryName+'-healthsites-shp'
    # resource_shp['format'] = 'zipped shapefile'
    # resource_shp['description'] = countryName+' healthsites shapefiles'

    # if open(configuration['data_folder']+'shapefiles.zip'):
    #     resource_shp.set_file_to_upload(configuration['data_folder']+'shapefiles.zip')

    if open(configuration['data_folder']+countryName+'.csv'):
        resource_csv.set_file_to_upload(configuration['data_folder']+countryName+'.csv')

    # if open(configuration['data_folder']+countryName+'.geojson'):
    #     resource.set_file_to_upload(configuration['data_folder']+countryName+'.geojson')

    # dataset.add_update_resources([resource,resource_csv,resource_shp])
    dataset.add_update_resource(resource_csv)

    return dataset
