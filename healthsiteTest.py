import requests
from hdx.configuration import Configuration
from hdx.data.dataset import Dataset
from slugify import slugify
import json

configuration = Configuration(hdx_site='test', hdx_keyfile ='.hdxkey',hdx_read_only=True, project_config_dict={})

dataset = Dataset.read_from_hdx('Liberia healthsites')
print('jeu de donnees :' +dataset.get_dataset_date())
# parametres = {'page':1, 'format':'geojson'}
# url = 'https://healthsites.io/api/v1/healthsites/facilities?'
# resource_url = url #+parametres['page']+'?'+parametres['format']
# #data = json.loads(response.text)
# # with open('data/healthfacilities.geojson', 'w') as f :
# #     json.dump(data,f)
#
# name = 'Health facilities in Africa'
# title = 'Health facilities in Africa by healthsite'
# slugified_name = slugify(title).lower()
#
# configuration = Configuration(hdx_site='test', hdx_keyfile ='.hdxkey',hdx_read_only=True, project_config_dict={})
#
# dataset = Dataset(configuration, {'name': slugified_name,'title': title})
# resources = [{'name':'healthfacilities','format':'geojson','url':resource_url}]
#
# dataset.update({'resource':resources})
#
# dataset.update({'owner_org': 'Global Healthsites Mapping Project','dataset_source': 'OSM','license_id': 'cc-by-sa'})
#
#
# dataset.resource.check_required_fields()
