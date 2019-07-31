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
import logging
import time
from hdx.facades.simple import facade
from healthsite2 import generate_dataset
from slugify import slugify
from hdx.data.dataset import Dataset
logger = logging.getLogger(__name__)


def main():
    '''Generate dataset and create it in HDX'''
    conf = Configuration()
    countries = {
            'Benin': 'BEN'
            # 'Burkina Faso': "BFA",
            # 'Burundi': "BDI",
            # 'Congo': "COG",
            # 'Ivory Coast': "CIV",
            # 'Guinea': "GIN",
            # 'Gambia': "GMB",
            # 'Liberia': "LBR",
            # 'Ghana': "GHA",
            # 'Guinea-bissau': "GNB",
            # 'Nigeria': "NGA", too large
            # 'Mali': "MLI",
            # 'Mauritania': "MRT",
            # 'Malawi': "MWI",
            # 'Marocco': "MAR",
            # 'Niger': "NER",
            # 'Senegal': "SEN",
            # 'Sierra Leone': "SLE",
            # 'Togo': "TGO",
            # 'Cameroon': "CMR",
            # 'Central African Republic': "CAF",
            # 'Tanzania': "TZA",
            # 'Rwanda': "RWA",
            #'Somalia': "SOM",
            #'South Sudan': "SSD",
            #'Yemen': "YEM",
            #'Democratic Republic of The Congo': "COD",
            # 'Uganda': "UGA",
            # 'Zambia': "ZMB",
            # 'Angola': "AGO",
            # 'Kenya': "KEN",
            # 'Ethiopia': "ETH",
            # 'Algeria': "DZA",
            # 'Egypt': "EGY",
            # 'Tunisia': "TUN",
            # 'Libya': "LBY",
            #'Sudan': "SDN",
            #'Bangladesh': "BGD",
            # 'Djibouti': "DJI",
            # 'Gabon': "GAB",
            # 'Madagascar': "MDG",
            # 'Lesotho': "LSO",
            # 'Namibia': "NAM",
            # 'Zimbabwe': "ZWE",
            #'Mozambique': "MOZ",
            # 'Botswana': "BWA",
            # 'Palestine': "PSE",
            # 'Mauritius': "MUS",
            # 'Zambia': "ZMB",
            # 'Cape Verde': "CPV",
            # 'Chad': "TCD",
            # 'Comoros': "COM",
            # 'Equatorial Guinea': "GNQ",
            # 'Eritrea': "ERI",
            # 'Syria': "SYR",
            # 'Jordan': "JOR",
            # 'Lebanon': "LBN",
            # 'Iraq': "IRQ",
            # 'Nepal': "NPL",
            #'Venezuela': "VEN",
            #'Philippines': "PHL",
            #'Afghanistan': "AFG",

            #OCHA ROLAC EXPORTs
            # 'Bolivia': "BOL",
            # 'Colombia': "COL",
            # 'Ecuador': "ECU",
            # 'El Savador': "SLV",
            # 'Guatemala': "GTM",
            # 'Haiti': "HTI",
            # 'Honduras': "HND",
            # 'Mexico': "MEX",
            # 'Nicaragua': "NIC",
            # 'Panama': "PAN",
            # 'Peru': "PER",
            # 'Dominican Republic': "DOM",
            # 'Trinidad and Tobago' : "TTO",
            # 'Barbados': "BRB",
            # 'Belize' : "BLZ",
            # 'Aruba': "ABW",
            # 'Grenada': "GRD",
            # 'Saint Vincent and the Grenadines': "VCT",
            #  'Saint Lucia': "LCA",
            # 'Martinique': "MTQ",
            # 'Dominica': "DMA",
            # 'Guadeloupe': "GLP",
            # 'Antigua and Barbuda': "ATG",
            # 'Montserrat': "MSR",
            # 'Saint Kitts and Nevis': "KNA",
            # 'Anguilla': "AIA",
            # 'British Virgin Islands': "VGB",
            # 'Puerto Rico': "PRI",
            # 'Jamaica': "JAM",
            # 'Turks and Caicos': "TCA",
            # 'Cayman Islands': "CYM",
            # 'Bahamas': "BHS",
            # 'Cuba': "CUB"


            # adhoc exports 
            # 'Indonesia': "IDN"
    }

    for pays in countries:
        # paysLower = slugify(pays).lower()
        dataset = generate_dataset(conf, pays)
        dataset.update_from_yaml()
        dataset.add_country_location(countries[pays])
        dataset.set_expected_update_frequency('Live')
        dataset.add_tags([pays,'hospitals', 'health facilities', 'HEALTHSITES'])
        datex = time.strftime("%x")
        dataset.set_dataset_date(datex)
        dataset.set_subnational(True)
        dataset.create_in_hdx()
        # try:
        #     old_dataset = Dataset.read_from_hdx(paysLower+'-healthsites')
        #     ressources = old_dataset.get_resources()
        #     for r in ressources:
        #         if r['name'] == pays+'-healthsites-csv':
        #             old_dataset.delete_resource(r)
        #     print('=== csv resource deleted ===')
        #     dataset = generate_dataset(conf, pays)
        #     dataset.update_from_yaml()
        #     dataset.add_country_location(countries[pays])
        #     dataset.set_expected_update_frequency('Live')
        #     dataset.add_tags([pays,'hospitals', 'health facilities', 'HEALTHSITES'])
        #     datex = time.strftime("%x")
        #     dataset.set_dataset_date(datex)
        #     dataset.set_subnational(True)
        #     dataset.create_in_hdx()
        # except Exception as e:
        #     continue

if __name__ == '__main__':
    facade(main, hdx_site='test', user_agent='HDXINTERNAL healthsites scraper', project_config_yaml=join('config', 'project_configuration.yml'))
