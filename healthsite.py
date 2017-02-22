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

    data = loaData.getDataByLoc(configuration['SEN_bbox'],configuration['base_url'])
    loaData.writeData(data,name)

    dataset = Dataset(configuration, {
        })

    date = time.strftime("%d/%m/%Y")
    dataset['dataset_date'] = date
    dataset.update_from_yaml()

    sen_resource = [{'name': name,
                'format': 'json',
                'url': configuration['base_url'],
                'description':'health facilities in Senegal',
                'url_type':'geojson'
                }]

    resource = Resource(sen_resource)
    print(resource)
    # resource.set_file_to_upload('data/dakar.geojson')
    dataset.add_update_resource(resource)

    return dataset
