#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
REGISTER:
---------

Caller script. Designed to call all other functions
that register datasets in HDX.

'''
import logging
from datetime import datetime
from hdx.data.dataset import Dataset
import time

from hdx.facades.scraperwiki import facade

from healthsite2 import generate_dataset
logger = logging.getLogger(__name__)
from hdx.configuration import Configuration
import subprocess
from slugify import slugify



def main():
    '''Generate dataset and create it in HDX'''
    conf = Configuration()

    countries = {
            # 'Benin': "BEN",
            # 'Burkina Faso': "BFA",
            # 'Ivory Coast': "CIV",
            # 'Ghana': "GHA",
            # 'Guinea': "GIN",
            # 'Guinea-bissau': "GNB",
            # 'Gambia': "GMB",
            # 'Liberia': "LBR",
            # 'Mali': "MLI",
            # 'Mauritania': "MRT",
            # 'Niger': "NER",
            # 'Nigeria': "NGA",
            # 'Senegal':"SEN",
            # 'Sierra Leone':	"SLE",
            # 'Togo': "TGO",
            # 'Cameroon': "CMR",
            # 'Central African Republic':"CAR",
            # 'Tanzania':"TZA",
            # 'Rwanda': "RWA",
            'Somalia': "SOM",
            'South Sudan': "SSD",
            'Yemen': "YEM"
    }

    for pays in countries:
        dataset = generate_dataset(conf,pays)
        dataset.update_from_yaml()
        dataset.add_country_location(countries[pays])
        dataset.set_expected_update_frequency('Every month')
        datex = time.strftime("%x")
        dataset.set_dataset_date(datex)
        dataset.add_tags([pays,'HEALTH','HEALTHSITES'])
        dataset.create_in_hdx()



if __name__ == '__main__':
    facade(main, hdx_site='prod')
