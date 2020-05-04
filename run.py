#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
REGISTER:
---------

Caller script. Designed to call all other functions
that register datasets in HDX.

'''
from hdx.hdx_configuration import Configuration
from os.path import join, expanduser
import os
import logging
import time
import csv
import requests
from hdx.facades.simple import facade
from healthsite2 import *
import pandas as pd
from hdx.utilities import *
# from hdx.data.dataset import Dataset
logger = logging.getLogger(__name__)
lookup = 'hdx-scraper-healthsite'


def checkCountryHealthsites(country):
    url = "https://healthsites.io/api/v2/facilities/count?api-key=" + getAPIKEY() + "&country=%s" % country
    return requests.get(url).status_code


def csvFile():
    print("Loarding file...")
    countries = pd.read_csv('Countries exports.csv', delimiter=',')
    countries['Status'] = countries['Country'].apply(lambda x: checkCountryHealthsites(x))

    country_to_export = countries[countries["Status"] == 200]
    country_to_export.to_csv("new_countries_to_export.csv")
    return country_to_export


def main():
    '''Generate dataset and create it in HDX'''
    conf = Configuration()
    # removing all files in dat directory
    if(os.path.isdir("data")):
        for fichier in os.listdir("data"):
            os.remove("data/" + fichier)

    #csvFile()
    countries = pd.read_csv('new_countries_to_export.csv', delimiter=',')
    # countries["Export"] = "to_export"
    for pays in countries.itertuples():
        print(pays[3])
        try:
            dataset = generate_dataset(conf, pays[2])
            dataset.update_from_yaml()
            dataset.add_country_location(pays[3])
            dataset.set_expected_update_frequency('Every month')
            dataset.add_tag('health facilities')
            datex = time.strftime("%x")
            dataset.set_dataset_date(datex)
            dataset.set_subnational(True)
            dataset.create_in_hdx()
        except Exception as e:
            print(e)
            continue




if __name__ == '__main__':

    facade(main, hdx_site='test', user_agent_config_yaml=join(expanduser('~'), '.useragent.yml'), user_agent_lookup=lookup, project_config_yaml=join('config', 'project_configuration.yml'))
