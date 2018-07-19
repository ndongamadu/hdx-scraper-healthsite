#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
REGISTER:
---------

Caller script. Designed to call all other functions
that register datasets in HDX.

'''
from os.path import join
import logging
from datetime import datetime
from hdx.data.dataset import Dataset
from hdx.data.resource import Resource
import time

from hdx.facades.simple import facade

from healthsite2 import generate_dataset
logger = logging.getLogger(__name__)
from hdx.hdx_configuration import Configuration
import subprocess
from slugify import slugify



def main():
    '''Generate dataset and create it in HDX'''
    conf = Configuration()
    countries = {
            # 'Benin': 'BEN',
            # 'Burkina Faso': "BFA",
            # 'Burundi': "BDI",
            # 'Congo': "COG",
            # 'Ivory Coast': "CIV",
            # 'Guinea': "GIN",
            # 'Gambia': "GMB",
            # 'Liberia': "LBR",
            # 'Ghana': "GHA",
            # 'Guinea-bissau': "GNB",
            # 'Nigeria': "NGA",
            
            #'Mali': "MLI",
            #'Mauritania': "MRT",
            #'Malawi':"MWI",
            #'Marocco': "MAR",
            'Niger': "NER",

            #'Senegal':"SEN",
            #'Sierra Leone': "SLE",
            #'Togo': "TGO",
            # 'Cameroon': "CMR",
            # 'Central African Republic':"CAR",
#            'Tanzania':"TZA",
#            'Rwanda': "RWA",
#            'Somalia': "SOM",
#            'South Sudan': "SSD",
#            'Yemen': "YEM",
#            'Democratic Republic of The Congo': "COD",
#            'Uganda': "UGA",
#            'Zambia': "ZMB",
#            'Angola': "AGO",
#            'Kenya': "KEN",
#            'Ethiopia': "ETH",
#            'Algeria': "DZA",
#            'Egypt': "EGY",
#            'Tunisia':"TUN",
#            'Haiti': "HTI",
#            'Libya': "LBY",
#            'Sudan': "SDN",
#            'Bangladesh': "BGD",
#            'Djibouti': "DJI",
#            'Gabon': "GAB",
#            'Madagascar': "MDG",
#            'Lesotho': "LSO",
#            'Namibia': "NAM",
#            'Zimbabwe': "ZWE",
#            'Mozambique': "MOZ",
#            'Botswana': "BWA",
#            'Palestine': "PSE",
#            'Mauritius' : "MUS",
#            'Zambia' : "ZMB",
#            'Cape Verde': "CPV",
#            'Chad': "TCD",
#            'Comoros':"COM",
#            'Equatorial Guinea': "GNQ",
#            'Eritrea' : "ERI",
#            'Syria': "SYR",
#            'Jordan': "JOR",
#            'Lebanon' : "LBN",
#            'Colombia':"COL",
#            'Iraq': "IRQ",
#            'Nepal': "NPL"

    }

    for pays in countries:
        paysLower = slugify(pays).lower()
        try:
            old_dataset = Dataset.read_from_hdx(paysLower+'-healthsites')
            ressources = old_dataset.get_resources()
            for r in ressources:
                if r['name'] == pays+'-healthsites-shp':
                    old_dataset.delete_resource(r)
        except Exception as e:
            raise e

        dataset = generate_dataset(conf,pays)
        dataset.update_from_yaml()
        dataset.add_country_location(countries[pays])
        dataset.set_expected_update_frequency('Live')
        dataset.add_tags([pays,'HEALTH','HEALTHSITES'])
        datex = time.strftime("%x")
        dataset.set_dataset_date(datex)
        
        dataset.create_in_hdx()



if __name__ == '__main__':
    facade(main, hdx_site='prod', user_agent='Healthsite data script',project_config_yaml=join('config', 'project_configuration.yml'))
