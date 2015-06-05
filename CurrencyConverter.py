#!/usr/bin/env python
#encoding: utf-8

"""
Currency Converter

Typing a currency and this little baby will convert other currencies.

I use this website: http://www.xe.com/currencyconverter/

Written by Tibor Oros, 2015 (oros.tibor0@gmail.com)

Recommended version: Python 2.7
"""

import json
import os
import sys

import requests
from bs4 import BeautifulSoup

CURR = 'EUR'

def fileOpen(fileName):
    if not(os.path.exists(fileName)):
        print 'File does not exists'
        sys.exit(1)
    f = open(fileName, 'r')
    data = json.loads(f.read())
    f.close()
    print 'Currency read Complete'
    return data

def find_td_element(c):
    r = requests.get('http://www.xe.com/currencyconverter/convert/?Amount=1&From={0}&To={1}'.format(CURR,c))
    l = BeautifulSoup(r.content)
    d = l.findAll('td')
    return d

def writeToFile(data, fileName):
    f = open(fileName, 'w')
    f.write(data)
    f.close()
    print 'Valute into File Complete'


#####################################################

#valute['EUR'] = 1.0
valute = {}
currencys = fileOpen('currencyList')

for currency in currencys:
    td_list = find_td_element(currency)
    
    for td in td_list:
        if td.get('class') is not None:
            if td.get('class')[0] in ['rightCol']:
                td_text = td.text.encode('utf-8')
                value = float(td_text.split(' ')[0].replace(',',''))
                if value == 0.0:
                    break
                valute[currency] = value
                print '{0} to {1}'.format(CURR, currency)
                break
            
#dict --> json   
data = json.dumps(valute)
writeToFile(data, 'valute')
