# from datetime import timedelta
#
# import requests
# from hdx.data.dataset import Dataset
# from slugify import slugify
# import json

import requests
from hdx.configuration import Configuration
from hdx.data.dataset import Dataset
from slugify import slugify
import json
#from hdx.facades.simple import facade

def generate_dataset(configuration):
    parametres = {'page':1, 'format':'geojson'}
    url = 'https://healthsites.io/api/v1/healthsites/facilities?'
    response = requests.get(url,params=parametres)
    data = json.loads(response.text)
    with open('data/healthfacilities.geojson', 'w') as f :
        json.dump(data,f)

    name = 'Health facilities in Africa'
    title = 'Health facilities in Africa by healthsite'
    slugified_name = slugify(title).lower()

    dataset = Dataset(configuration, {
            'name': slugified_name,
            'title': title,
        })

    dataset.update({
        'owner_org': 'Global Healthsites Mapping Project'
        'dataset_source': 'OSM'
        'license_id': 'cc-by-sa'
        })

    dataset.resource.check_required_fields()
