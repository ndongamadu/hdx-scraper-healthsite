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

from hdx.facades.scraperwiki import facade

from healthsite import generate_dataset

logger = logging.getLogger(__name__)
from hdx.configuration import Configuration



def main():
    '''Generate dataset and create it in HDX'''
    conf = Configuration()
    countries = {
            'Benin': "BEN",
            'Burkina Faso': "BFA",
            'Ivory-coast': "CIV",
            'Ghana': "GHA",
            'Guinea': "GIN",
            'Gambia': "GMB",
            'Guinea-Bissau': "GNB",
            'Liberia': "LBR",
            'Mali': "MLI",
            'Mauritania': "MRT",
            'Niger': "NER",
            'Nigeria': "NGA",
            'Senegal': "SEN",
            'Sierra Leone': "SLE",
            'Togo': "TGO"
    }

    for pays in countries:
        dataset = generate_dataset(conf,pays)
        dataset.update_from_yaml()
        dataset.add_country_location(countries[pays])
        # dataset.create_in_hdx()
        print('dataset ajoute !')


if __name__ == '__main__':
    facade(main, hdx_site='prod')
