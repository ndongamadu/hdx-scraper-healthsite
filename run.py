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
    dataset = generate_dataset(conf)
    dataset.update_from_yaml()
    dataset.create_in_hdx()


if __name__ == '__main__':
    facade(main, hdx_site='feature')
