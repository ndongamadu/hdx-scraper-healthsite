#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
REGISTER:
---------

Caller script. Designed to call all other functions
that register datasets in HDX.

'''
from hdx.hdx_configuration import Configuration
from os.path import join
import os
import logging
import time
import csv
import requests
from hdx.facades.simple import facade
from healthsite2 import generate_dataset
from slugify import slugify
from hdx.data.dataset import Dataset
logger = logging.getLogger(__name__)


def main():
    '''Generate dataset and create it in HDX'''
    conf = Configuration()
    #removing all files in dat directory 
    if(os.path.isdir("data")):
        for fichier in os.listdir("data"):
            os.remove("data/"+fichier)
    #getting the list of countries to export
    countriesListURL = 'https://proxy.hxlstandard.org/data.csv?strip-headers=on&url=https%3A%2F%2Fdocs.google.com%2Fspreadsheets%2Fd%2F1UFo-3Ow9AT7uEC5Xc_ugB8o21DJFKjlwcRZF1dNPgGA%2Fedit%3Fusp%3Dsharing&force=on'
    response = requests.get(countriesListURL)
    wrapper = csv.reader(response.text.strip().split('\n'))
    countries = []
    for record in wrapper:
        if record[0] != '#country+name':
            countries.append(record)

    for pays in countries:
        dataset = generate_dataset(conf, pays[0])
        dataset.update_from_yaml()
        dataset.add_country_location(pays[0])
        dataset.set_expected_update_frequency('Live')
        dataset.add_tag('health facilities')
        datex = time.strftime("%x")
        dataset.set_dataset_date(datex)
        dataset.set_subnational(True)
        dataset.create_in_hdx()

if __name__ == '__main__':
    facade(main, hdx_site='test', user_agent='HDXINTERNAL healthsites scraper', project_config_yaml=join('config', 'project_configuration.yml'))
