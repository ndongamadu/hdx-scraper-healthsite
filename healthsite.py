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

    url = configuration['base_url']+configuration['api']
    loaData.getAllHealthSitePageData(url)

    name = 'Africa health facilities'
    title = 'Africa health facilities data'
    slugified_name = slugify(name).lower()
    dataset = Dataset(configuration, {

    })
    dataset['name'] = slugified_name
    dataset['title'] = title
    date = time.strftime("%d/%m/%Y")
    dataset['dataset_date'] = date
    dataset.add_continent_location('AF')

    rName = "health facilities"
    resource = Resource()
    resource['name'] = rName
    resource['format'] = 'geojson'
    resource['url'] = url
    resource['description'] = configuration['base_url']
    resource['url_type'] = 'api'
    resource['resource_type'] = 'api'
    resource.set_file_to_upload(configuration['data_folder']+'healthfacilities.geojson')

    dataset.add_update_resource(resource)

    return dataset
