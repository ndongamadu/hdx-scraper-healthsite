"""
healthsites API documentation
https://github.com/healthsites/healthsites/wiki/API
https://healthsites.io/api/v1/healthsites/search?search_type=facility&name=benin&format=json
"""
import logging
from hdx.data.dataset import Dataset
from hdx.data.resource import Resource
import requests
from slugify import slugify
import json
import csv
import os
import shutil
import subprocess

logger = logging.getLogger(__name__)

# https://healthsites.io/api/v1/healthsites/search?search_type=placename&format=geojson$name=

# create the data folder


def getCountryHealthSites(configuration, countryName):
    print('<------- Generating %s dataset -------->' % countryName)

    url = configuration.read()['base_url'] + configuration.read()['api_version'] + configuration.read()['api_name'] + "search?search_type=placename&format=geojson"
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
    # if(len(newData['features'])> len(countryData['features'])):
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
    #rename the geojson to the country name
    shutil.move(configuration.read()['data_folder']+"healthsites.geojson", configuration.read()['data_folder']+countryName+".geojson")
    
    reader = csv.reader(open(configuration.read()['data_folder']+"healthsites.csv"))
    nbRows = 0
    with open(configuration.read()['data_folder']+countryName+".csv", 'w') as fcsv:
        writer = csv.writer(fcsv, delimiter=',')
        for raw in reader:
            if nbRows == 0 :
                writer.writerow(raw)
                writer.writerow(["#geo +lon","#geo +lat","#meta +osm_id","#meta +source_url"," "," ","#loc +name", "#indicator +completeness", "#meta +uuid", "#date", "#meta +source", "#meta +osm_type", "#meta +version", "#indicator +type", " ", " ", "#contact +phone", " ", "#meta +opening_hours", "#contact +email"])
                nbRows +=1
            else:
                writer.writerow(raw)
    if(os.path.isfile(configuration.read()['data_folder']+"healthsites.csv")):
        os.remove(configuration.read()['data_folder']+"healthsites.csv")
    print("===== %s files generated ! ======" %countryName)

def generate_dataset(configuration,countryName):
    #showedName = countryName
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
        geojsonResource.set_file_to_upload(configuration.read()['data_folder']+countryName+'.geojson')

        geojsonResource.check_required_fields(['group','package_id'])
        dataset.add_update_resource(geojsonResource)
    #csv resource
    if(os.path.isfile(configuration.read()['data_folder']+countryName+'.csv')):
        resource_csv = Resource()
        resource_csv['name'] = countryName+'-healthsites-csv'
        resource_csv['description'] = countryName+' healthsites csv'
        resource_csv['format'] = 'csv'
        resource_csv.set_file_to_upload(configuration.read()['data_folder']+countryName+'.csv')

        resource_csv.check_required_fields(['group','package_id'])
        dataset.add_update_resource(resource_csv)
    # shp resource
    if(os.path.isfile(configuration.read()['data_folder']+countryName+"-shapefiles.zip")):
        resource_shp = Resource()
        resource_shp['name'] = countryName+'-healthsites-shp'
        resource_shp['format'] = 'zipped shapefile'
        resource_shp['description'] = countryName+' healthsites shapefiles'
        resource_shp.set_file_to_upload(configuration.read()['data_folder']+countryName+"-shapefiles.zip")

        resource_shp.check_required_fields(['group','package_id'])
        dataset.add_update_resource(resource_shp)

    return dataset
