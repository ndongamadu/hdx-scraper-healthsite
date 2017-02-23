import logging
from hdx.data.dataset import Dataset
from hdx.data.resource import Resource
import requests
from slugify import slugify
import json
import time

import loaData

logger = logging.getLogger(__name__)

def generate_dataset(configuration):

    name = "sen-healthfacilities"
    url = configuration['base_url']+configuration['api']
    data = loaData.getDataByLoc(configuration['SEN_bbox'],url)
    loaData.writeData(data,name)

    dataset = Dataset(configuration, {
        })

    date = time.strftime("%d/%m/%Y")
    dataset['dataset_date'] = date
    dataset.update_from_yaml()

    resource = Resource()
    resource['name'] = name
    resource['format'] = 'geojson'
    resource['url'] = url
    resource['description'] = configuration['base_url']
    resource['url_type'] = 'api'
    resource['resource_type'] = 'api'
    resource.set_file_to_upload(configuration['data_folder']+name+'geojson')

    resource.check_required_fields()
    dataset.add_update_resource(resource)

    return dataset
