'''
change update frequency to live for all the healhsites datasets
'''

import logging
from datetime import datetime
from hdx.data.dataset import Dataset
import time

from hdx.facades.scraperwiki import facade

from healthsite2 import generate_dataset
logger = logging.getLogger(__name__)
from hdx.configuration import Configuration
from slugify import slugify

def main():
    conf = Configuration()
    
    countries = {
              'Benin': "BEN",
#              'Burkina Faso': "BFA",
#             'Burundi': "BDI",
#             'Congo': "COG",
#              'Ivory Coast': "CIV",
              'Ghana': "GHA"
#              'Guinea': "GIN",
#              'Guinea-bissau': "GNB",
#              'Gambia': "GMB",
#              'Liberia': "LBR",
#              'Mali': "MLI",
#              'Mauritania': "MRT",
#             'Malawi':"MWI",
#             'Marocco': "MAR",
#              'Niger': "NER",
#              'Nigeria': "NGA",
#              'Senegal':"SEN",
#              'Sierra Leone': "SLE",
#              'Togo': "TGO",
#              'Cameroon': "CMR",
#              'Central African Republic':"CAR",
#              'Tanzania':"TZA",
#              'Rwanda': "RWA",
#              'Somalia': "SOM",
#              'South Sudan': "SSD",
#              'Yemen': "YEM",
#              'Democratic Republic of The Congo': "COD",
#              'Uganda': "UGA",
#              'Zambia': "ZMB",
#              'Angola': "AGO",
#              'Kenya': "KEN",
#              'Ethiopia': "ETH"
#              'Algeria': "DZA",
#              'Egypt': "EGY",
#             'Tunisia':"TUN"
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
#            'Botswana': "BWA"
#            'Palestine': "PSE",
#            'Mauritius' : "MUS",
#            'Zambia' : "ZMB"
        
    }
    
    dataset = Dataset.read_from_hdx('zimbabwe-healthsites')
    
#    for pays in countries:
#        showedName = pays
#        if(pays=="Ivory Coast"):
#            showedName="Cote d'Ivoire"
#        name = showedName+'-healthsites'
#        dataset = Dataset.read_from_hdx(name)
#        print(dataset)
#        print("Done")
    
if __name__ == '__main__':
    facade(main, hdx_site='test')