# from datetime import timedelta
#
# import requests
# from hdx.data.dataset import Dataset
# from slugify import slugify
# import json

import logging
from hdx.data.dataset import Dataset
import requests
from slugify import slugify
import json
import time
#from hdx.facades.simple import facade


logger = logging.getLogger(__name__)

def generate_dataset(configuration):
    parametres = {'page':1, 'format':'geojson'}
    url = 'https://healthsites.io/api/v1/healthsites/facilities?page=1&format=json'
    # response = requests.get(url,params=parametres)
    # data = json.loads(response.text)
    # with open('data/healthfacilities.geojson', 'w') as f :
    #     json.dump(data,f)

    name = 'Health facilities in Africa'
    # title = 'Health facilities in Africa by healthsite'
    # slugified_name = slugify(title).lower()

    dataset = Dataset(configuration, {
        })

    # dataset['name'] = slugified_name
    # dataset['title'] = title
    date = time.strftime("%d/%m/%Y")
    dataset['dataset_date'] = date
    dataset.update_from_yaml()
    resources = [{
        'name': name,
        'format': 'json',
        'url': url
    }]

    for resource in resources:
        resource['description'] = resource['url'].rsplit('/', 1)[-1]
        resource['url_type'] = 'api'
        resource['resource_type'] = 'api'

    # dataset.update({
    #     'owner_org': 'Global Healthsites Mapping Project'
    #     'dataset_source': 'OSM'
    #     'license_id': 'cc-by-sa'
    #     })

    # dataset.resource.check_required_fields()
    # resources.set_file_to_upload('data/healthfacilities.geojson')
    dataset.add_update_resources(resources)

    return dataset
