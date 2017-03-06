import logging
from hdx.data.dataset import Dataset
from hdx.data.resource import Resource
import requests
from slugify import slugify
import json
import time
import csv

logger = logging.getLogger(__name__)

def writeCsv(countryName):
    print('<------ creating csv file ------->')
    try:
        fichier = open('data/'+countryName+'.geojson')
        fd = json.load(fichier)
        countryData = fd['features']

        csvf = open('data/'+countryName+'.csv','w')
        csvwriter = csv.writer(csvf)
        csvwriter.writerow(('tpe','lat','lon','name','version','completeness','source_url','raw_source','what3words','uuid','source','typeP','upstream','date_modified'))

        for jdkeys in countryData:
            geom = jdkeys['geometry']
            prop = jdkeys['properties']

            coord = geom['coordinates']
            tpe = geom['type']
            completeness = prop['completeness']
            source_url = prop['source_url']
            try:
                raw_source = prop['raw-source']
            except Exception :
                pass
            what3words = prop['what3words']
            uuid = prop['uuid']
            source = prop['source']
            try:
                typeP = prop["type"]
            except Exception:
                pass
            upstream = prop['upstream']
            date_modified = prop['date_modified']
            name = prop['name']
            version = prop['version']
            csvwriter.writerow((tpe,coord[0],coord[1],name,version,completeness,source_url,raw_source,what3words,uuid,source,typeP,upstream,date_modified))
    except Exception as e:
        print('sorry csv not created')
    print('<----- csv created ----->')

def generateCountryDataset(countryName,format):
    countries = {
    'Benin':"Cotonou",
    'Burkina Faso':"Ouagadougou",
    'Ivory-coast' : "Abidjan",
    'Ghana': "accra",
    'Guinea': "conakry",
    'Gambia': "banjul",
    'Guinea-Bissau': "bissau",
    'Liberia': "monrovia",
    'Mali': "bamako",
    'Mauritania': "nouatchott",
    'Niger': "niamey",
    'Nigeria': "lagos",
    'Senegal': "dakar",
    'Sierra Leone': "freetown",
    'Togo' : "lome"
    }
    capitale = countries[countryName]
    print('<------- Generating %s dataset -------->' %countryName)
    url ="https://healthsites.io/api/v1/healthsites/search?search_type=placename"
    parametres = {'name':countryName+'-'+capitale,'format':format}
    countryData = {"type": "FeatureCollection", "features": []}

    try:
        with open('data/'+countryName+'.geojson','r') as f:
            countryData = json.load(f)
    except Exception as e:
        pass

    try:
        response = requests.get(url,params=parametres)
        data = json.loads(response.text)
        if(len(data['features'])>len(countryData['features'])):
            with open('data/'+countryName+'.geojson','w') as f:
                json.dump(data,f)
                print('<------- File created in data folder --------->')
        else:
            print('File exists yet & there is no updates')
        writeCsv(countryName)

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
    date = time.strftime("%d/%m/%Y")
    dataset['dataset_date'] = date

    rName = countryName+'-healthsites-geojson'
    resource = Resource()
    resource['name'] = rName
    resource['format'] = 'geojson'
    resource['url'] = configuration['base_url']#+configuration['api']
    resource['description'] = configuration['base_url']
    resource['url_type'] = 'api'
    resource['resource_type'] = 'api'

    generateCountryDataset(countryName,resource['format'])
    # writeCsv(countryName)
    resource_csv = Resource()
    resource_csv['name'] = countryName+'-healthsites-csv'
    resource_csv['url'] = configuration['base_url']
    resource_csv['description'] = configuration['base_url']
    resource_csv['url_type'] = 'api'
    resource_csv['resource_type'] = 'api'
    resource_csv['format'] = 'csv'
    resource_csv.set_file_to_upload(configuration['data_folder']+countryName+'.csv')
    # resource_csv.create_datastore(schema={'tpe':'STRING','lat':'STRING','lon':'STRING',
    #     'name':'STRING','version':'STRING','completeness':'STRING','source_url':'STRING',
    #     'raw_source':'STRING','what3words':'STRING','uuid':'STRING','source':'STRING','typeP':'STRING',
    #     'upstream':'STRING','date_modified':'STRING'},path=configuration['data_folder']+countryName+'.'+resource['format'])

    resource.set_file_to_upload(configuration['data_folder']+countryName+'.'+resource['format'])

    dataset.add_update_resources([resource,resource_csv])

    return dataset
