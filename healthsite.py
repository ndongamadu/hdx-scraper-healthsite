import logging
from hdx.data.dataset import Dataset
from hdx.data.resource import Resource
import requests
from slugify import slugify
import json
import time

logger = logging.getLogger(__name__)

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
    try:
        response = requests.get(url,params=parametres)
        data = json.loads(response.text)
        with open('data/'+countryName+'.geojson','w') as f:
            json.dump(data,f)
        print('<------- File created in data folder --------->')
    except Exception as e:
        print('>---- pays non reconnu ----<')
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

    rName = countryName+'-healthsites'
    resource = Resource()
    resource['name'] = rName
    resource['format'] = 'geojson'
    resource['url'] = configuration['base_url']#+configuration['api']
    resource['description'] = configuration['base_url']
    resource['url_type'] = 'api'
    resource['resource_type'] = 'api'

    generateCountryDataset(countryName,resource['format'])

    resource.set_file_to_upload(configuration['data_folder']+countryName+'.'+resource['format'])

    dataset.add_update_resource(resource)

    return dataset
