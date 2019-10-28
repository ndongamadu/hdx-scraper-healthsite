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
import yaml
logger = logging.getLogger(__name__)

# https://healthsites.io/api/v1/healthsites/search?search_type=placename&format=geojson$name=
# https://healthsites.io/api/v2/facilities/?api-key=6e6169fb0ff9d2e2a590ca44ef1bae19af102205&country=senegal&output=geojson
# https://healthsites.io/api/v2/facilities/?api-key=6e6169fb0ff9d2e2a590ca44ef1bae19af102205&output=geojson&page=1&flat-properties=true


def getAPIKEY():
    apiFile = yaml.load(open('config/api-key.yml', 'r'))
    return apiFile['cle']


def getCountryHealthSites(configuration, countryName):
    print('<------- Generating %s dataset -------->' % countryName)

    url = configuration.read()['base_url'] + configuration.read()['api_version'] + configuration.read()['api_name'] + "?api-key=" + getAPIKEY() + "&output=geojson&flat-properties=true"
    countryData = {"type": "FeatureCollection", "features": []}
    try:
        with open('data/' + countryName + '.geojson', 'r') as f:
            countryData = json.load(f)
    except Exception:
        pass
    newData = {"type": "FeatureCollection", "features": []}
    parameters = {'country': countryName, 'page': 0}
    nbPage = 1
    # iterate on page number
    # get data by page and return newData with all the data
    while 1:
        parameters['page'] = nbPage
        response = requests.get(url, params=parameters)
        print(response.text)
        data = json.loads(response.text)
        # data = response.json()
        if(data['features'] == []):
            break
        else:
            for dt in data['features']:
                newData['features'].append(dt)
            nbPage += 1
    # write if newData different from the potential existing file (update)
    # if(len(newData['features'])> len(countryData['features'])):
        # write the file to use to create de shp
    with open(configuration.read()['data_folder'] + 'healthsites.geojson', 'w') as f:
        json.dump(newData, f)
    # write the geojson with the country name
    with open(configuration.read()['data_folder'] + countryName + '.geojson', 'w') as f2:
        json.dump(newData, f2)
    # write to csv
    subprocess.call("./geojsonToCSV.sh", shell=True)
    # write the shp
    subprocess.call("./writeToSHP.sh", shell=True)
    # rename the shp to the country name
    if(os.path.isfile(configuration.read()['data_folder'] + "shapefiles.zip")):
        shutil.move(configuration.read()['data_folder'] + "shapefiles.zip", configuration.read()['data_folder'] + countryName + "-shapefiles.zip")
    # rename the geojson to the country name
    shutil.move(configuration.read()['data_folder'] + "healthsites.geojson", configuration.read()['data_folder'] + countryName + ".geojson")

    # rename the csv to the country name
    if(os.path.isfile(configuration.read()['data_folder'] + "healthsites.csv")):
        shutil.move(configuration.read()['data_folder'] + "healthsites.csv", configuration.read()['data_folder'] + countryName + ".csv")

# adding hxl tags ?
    # reader = csv.reader(open(configuration.read()['data_folder']+"healthsites.csv"))
    # nbRows = 0
    # with open(configuration.read()['data_folder']+countryName+".csv", 'w') as fcsv:
    #     writer = csv.writer(fcsv, delimiter=',')
    #     for raw in reader:
    #         if nbRows == 0 :
    #             writer.writerow(raw)
    #             print(raw)
    #             writer.writerow(["#geo +lon","#geo +lat","#meta +osm_id","#meta +source_url","#geo +w3w"," ","#loc +name", "#indicator +completeness +pct", "#meta +uuid", "#date +modified", "#meta +source", "#meta +osm_type", "#meta +version", "#indicator +loctype", "#contact +phone", "#contact +address ", "#contact +email","#access +opening_hours",])
    #             nbRows +=1
    #         else:
    #             writer.writerow(raw)

    # ===
    #rename the csv to the country name
    # if(os.path.isfile(configuration.read()['data_folder']+"healthsites.csv")):
    #     shutil.move(configuration.read()['data_folder']+"healthsites.csv", configuration.read()['data_folder']+countryName+".csv")
    # ==
    # if(os.path.isfile(configuration.read()['data_folder']+"healthsites.csv")):
    #     os.remove(configuration.read()['data_folder']+"healthsites.csv")
    print("===== %s files generated ! ======" %countryName)
# ['X', 'Y', 'osm_id', 'source_url', 'what3words', 'upstream', 'name', 'completeness', 'uuid', 'date_modified', 'source', 'osm_type', 'version', 'type', 'defining-hours', 'activities', 'ownership', 'tags', 'scope-of-service', 'ancillary-services', 'phone', 'notes', 'nature-of-facility', 'physical-address', 'inpatient-service']


def hxlator(to_hxl):
    i = 0
    hxl_tags = [None] * len(to_hxl)
    print(hxl_tags)
    while i <= len(to_hxl):
        if to_hxl[i] == 'X':
            hxl_tags[i] = "#geo +lon"
        i += 1
    print("==hxl tags==")
    print(hxl_tags)


def generate_dataset(configuration, countryName):
    # showedName = countryName
    if(countryName == "Ivory Coast"):
        showedName = "Cote d'Ivoire"
    name = countryName + '-healthsites'
    title = countryName + '-healthsites'
    slugified_name = slugify(name).lower()
    # dataset = Dataset(configuration, {
    # })
    dataset = Dataset({
        'name': slugified_name,
        'title': title,
    })
    # dataset['name'] = slugified_name
    # dataset['title'] = title
    # generating the datasets
    getCountryHealthSites(configuration, countryName)
    # geojson resource
    if(os.path.isfile(configuration.read()['data_folder'] + countryName + '.geojson')):
        rName = countryName + '-healthsites-geojson'
        geojsonResource = Resource()
        geojsonResource['name'] = rName
        geojsonResource['format'] = 'geojson'
        geojsonResource['url'] = configuration.read()['base_url']
        geojsonResource['description'] = countryName + ' healthsites geojson'
        geojsonResource.set_file_to_upload(configuration.read()['data_folder'] + countryName + '.geojson')

        geojsonResource.check_required_fields(['group', 'package_id'])
        dataset.add_update_resource(geojsonResource)
    # csv resource
    if(os.path.isfile(configuration.read()['data_folder'] + countryName + '.csv')):
        resource_csv = Resource()
        resource_csv['name'] = countryName + '-healthsites-csv'
        resource_csv['description'] = countryName + ' healthsites csv'
        resource_csv['format'] = 'csv'
        resource_csv.set_file_to_upload(configuration.read()['data_folder'] + countryName + '.csv')

        resource_csv.check_required_fields(['group', 'package_id'])
        dataset.add_update_resource(resource_csv)
    # shp resource
    if(os.path.isfile(configuration.read()['data_folder'] + countryName + "-shapefiles.zip")):
        resource_shp = Resource()
        resource_shp['name'] = countryName + '-healthsites-shp'
        resource_shp['format'] = 'zipped shapefile'
        resource_shp['description'] = countryName + ' healthsites shapefiles'
        resource_shp.set_file_to_upload(configuration.read()['data_folder'] + countryName + "-shapefiles.zip")

        resource_shp.check_required_fields(['group', 'package_id'])
        dataset.add_update_resource(resource_shp)

    return dataset
