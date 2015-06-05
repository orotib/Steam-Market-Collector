#!/usr/bin/env python
#encoding: utf-8

"""
Steam Data Collector

Collecting data from Steam Market.

Do not use illegal activity! (e.g.: Steam Buyer Bot)

Written by Tibor Oros, 2015 (oros.tibor0@gmail.com)

Recommended version: Python 2.7
"""

import datetime
import json
import os
import random
import sys
import time


from bs4 import BeautifulSoup
import requests

def readURL(URL):
    while(1):
        try:
            r = requests.get(URL)
            l = BeautifulSoup(r.content)
            break
        except:
            print 'Connection error'
            time.sleep(30)

    #if we try too fast
    if l.text.encode('utf-8').find('Please wait and try your request again later.') != -1:
        print 'REQUEST DENIED'
        for i in xrange(10):
            print 'Waiting {0}s'.format(i*30)
            time.sleep(30)
        return 'WAIT'
    
    #if no offers for skins (dead link)
    elif l.text.encode('utf-8').find('There are no listings for this item') != -1:
        return 'DEAD'
    
    data = l.findAll('span')
    return data

def getvalutes():
    infile = open('valute', 'r').read()
    data = json.loads(infile)
    return data

def importLinks(fileName):
    f = open(fileName, 'r')
    data = [i.strip() for i in f.readlines()]
    return data

def loging(url, tmp):
    print '!!! ' + tmp + ' !!!'
    log = open('log','a')
    log.write('{0}\t{1}\n'.format(url, tmp))
    log.close()

def valutesToEur(tmp):
    try:
        if tmp.find('CDN') != -1:
            return (float(tmp.split(' ')[1].replace(',','.'))/valutes['CAD'])
        elif tmp.find('pуб') != -1:
            return (float(tmp.split(' ')[0].replace(',','.'))/valutes['RUB'])
        elif tmp.find('€') != -1:
            return (float(tmp.replace('€','').replace(',','.'))/valutes['EUR'])
        elif tmp.find('USD') != -1:
            return (float(tmp.split(' ')[0].replace('$','').replace(',','.'))/valutes['USD'])
        elif tmp.find('฿') != -1:
            return (float(tmp.replace('฿','').replace(',',''))/valutes['THB'])
        elif tmp.find(' TL') != -1:
            return (float(tmp.split(' ')[0].replace(',',''))/valutes['TRY']/100)
        elif tmp.find('¥') != -1:
            return (float(tmp.split(' ')[1].replace(',',''))/valutes['JPY'])
        elif tmp.find('R$') != -1:
            return (float(tmp.split(' ')[1].replace(',',''))/valutes['BRL']/100)
        elif tmp.find('£') != -1:
            return (float(tmp.replace('£',''))/valutes['GBP'])
        elif tmp.find('S$') != -1:
            return (float(tmp.replace('S$',''))/valutes['SGD'])
        elif tmp.find('P') != -1:
            return (float(tmp.replace('P','').replace(',',''))/valutes['PHP'])
        elif tmp.find('kr') != -1:
            return (float(tmp.replace(' kr','').replace('.','').replace(',','.'))/valutes['SEK'])
        elif tmp.find('RM') != -1:
            return (float(tmp.replace('RM','').replace(',',''))/valutes['MYR'])
        elif tmp.find('Rp') != -1:
            return (float(tmp.replace('Rp ','').replace(' ',''))/valutes['IDR'])
        elif tmp.find('NZ$') != -1:
            return (float(tmp.replace('NZ$ ',''))/valutes['NZD'])
        elif tmp.find('Mex$') != -1:
            return (float(tmp.replace('Mex$ ','').replace(',',''))/valutes['MXN'])
        elif tmp.find('Sold') != -1:
            return 5014.0
        else:
            print 'Something Else'
            loging(t_url, tmp)
    except:
        print 'Exception'
        loging(t_url, tmp)

    return 10000.0
    
def getPrices(li):
    #odd  --> real price
    #even --> seller gets
    pli = li[::2]
    pli.sort()
    return pli

def readable(url):
    tmp_list = url.split('/')
    name = tmp_list[-1]
    return name.replace('%E2%98%85','KNIFE ; ').replace('%E2%84%A2%20', ' ; ').replace(
                        '%20%7C%20',' ; ').replace('%20%28', ' ; ').replace('%20', ' ').replace('%29', '')

def getCategory(url):
    if url.find('StatTrak') != -1:
        return 'StatTrak'
    if url.find('Souvenir') != -1:
        return 'Souvenir'
    if url.find('%E2%98%85') != -1:
        return 'Knife'
    return 'normal'


#####################################################################

links = importLinks('links')

k = 0
print '*'*20 + ' SHUFFLE ' + '*'*20
#shuffle the links, because this is gambling
random.shuffle(links)

for t_url in links:
    #people changing, currency changing... sometimes too fast
    if not(k % 50):
        os.system('python CurrencyConverter.py')
        valutes = getvalutes()

    k += 1
    values = []
    #wait because the steam will be disabled
    time.sleep(round(random.uniform(10,15),2))
    print '{0}.\t{1}'.format(k,readable(t_url))

    span_list = readURL(t_url)
    if span_list == 'DEAD':
        print '*** Dead Link ***'
        continue
    if span_list == 'WAIT':
        print '*** Slower man ***'
        continue
    
    for span in span_list: 
        if span.get('class') is not None:
            if span.get('class')[0] in ['market_listing_price']:
                value = span.text.encode('utf-8').strip().replace('-','')
                values.append(valutesToEur(value))
                
    prices = getPrices(values)
    for i in prices:
        print str(round(i,2)) + ' |',
    print
