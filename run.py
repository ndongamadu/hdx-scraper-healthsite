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

from healthsite import generate_dataset
import pandas as pd
logger = logging.getLogger(__name__)
from hdx.configuration import Configuration
import subprocess



def main():
    '''Generate dataset and create it in HDX'''
    conf = Configuration()

    countries = {
            'Benin': "BEN",
            'Burkina Faso': "BFA",
            'ivory-coast': "CIV",
            'Ghana': "GHA",
            'Guinea republic': "GIN",
            'Gambia': "GMB",
            'Guinea Bissau republic': "GNB",
            'Liberia': "LBR",
            # 'Mali': "MLI",
            'Mauritania': "MRT",
            'Niger': "NER",
            'Nigeria': "NGA",
            'Senegal':"SEN",
            'Sierra Leone':	"SLE",
            'Togo': "TGO",
            'Cameroon': "CMR",
            'Central African Republic':"CAR"
    }

    for pays in countries:
        dataset = generate_dataset(conf,pays)
        dataset.update_from_yaml()
        dataset.add_country_location(countries[pays])
        dataset.set_expected_update_frequency('Every week')
        datex = time.strftime("%x")
        dataset.set_dataset_date(datex)
        dataset.add_tags([pays,'HEALTH','HEALTHSITES'])
        dataset.create_in_hdx()
        if open('data/shapefiles.zip') :
            subprocess.call("./clean.sh", shell=True)

        print('dataset ajoute !')


if __name__ == '__main__':
    facade(main, hdx_site='prod')
