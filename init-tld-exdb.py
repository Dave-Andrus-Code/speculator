# INIT-TLD-EXDB
# Written by DMA on 2022-11-20
# INITialize Top Level Domain EXpiration DataBases
# Creates dictionaries of domains by TLD for unique words.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# -----------------------------------------------------

import json
from os.path import exists
from datetime import date

# -----------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------

def FilterDomain(w1, w2, w3):
    # check if the words used to create a domain are usable

    # strip random spaces which can't be in domain names
    w1 = w1.replace(' ', '')
    w2 = w2.replace(' ', '')
    w3 = w3.replace(' ', '')

    if w1 != '':
        if w2 == '' and w3 == '':
            1 == 1 # do nothing; need to check the length
        if w2 == '' and w3 != '':
            return False    # I don't want to support this use case
        if w2 != '' and w3 != '':
            1 == 1 # do nothing; need to check the length
        if w2 != '' and w3 == '':
            1 == 1 # do nothing; need to check the length
    else:
        return False    # There has to be at least one word

    if len(w1 + w2 + w3) > 17:
        return False    # Too long domains are too long

    # If we made it this far, it's OK
    return True

def readczds(tld):
    # Read a zone file and return a dictionary object of unique domains
    dfn = 'e:\\data\\domain\\' + tld + '.dict'
    zfn = 'e:\\data\\domain\\' + tld + '.txt'

    # Initialize an empty dictionary that we can return no matter what
    dict = {}

    if exists(dfn):
        # get the dictionary if it has already been created previously
        print ('Loading dictionary ', dfn)
        with open(dfn, 'r') as f:
            dict = json.loads(f.read())
    else:
        if exists(zfn):
            # If the zone dictionary doesn't already exist, try to create one
            # from the DNS zone file
            with open(zfn, 'r') as f:
                z = f.readlines()
            for x in z:
                xs = x.replace('\t', ' ').split(' ')
                if xs[0][-1:] == '.':
                    xs[0] = xs[0][:len(xs[0])-1]
                dict[xs[0]] = 1
            print('Writing dictionary ', dfn)
            with open(dfn, 'w') as f:
                f.write(json.dumps(dict))
        else:
            print ('No zone data for ', tld)
    return dict

# -----------------------------------------------------
# MAIN
# -----------------------------------------------------

pdoms = {}      # potential domains words; single english words and
                # multi-word combos made up of 3 words or less
                # and whose length doesn't exceed 17 characters

domains = {}    # pdoms with tlds

# The top TLD's based on indexed pages and registrations
TLDS = [
    'COM',
    'NET',
    #'CO',
    'ORG',
    'XYX',
    'IO',
    'ME',
    'INFO',
    #'IN',
    'TOP',
    #'EU',
    #'AI',
    'ONLINE',
    #'US',
    'BIZ',
    #'GG',
    'TECH',
    #'TV',
    #'CC',
    'DEV',
    'CLUB',
    'APP',
    #'PW',
    'PRO',
    'SITE',
    #'CA',
    'SHOP',
    #'UK',
    'CO.UK',
    #'WIN',
    'STORE',
    'SPACE',
    'DOWNLOAD',
    #'ES',
    #'IT',
    'WORK',
    'CLOUD',
    'LIVE',
    #'WS',
    #'RU',
    #'IM',
    'ONE',
    'LIFE',
    'LINK'
    #'JP',
    #'DE',
    #'FR',
    #'BR',
    #'GOV',
    #'PL',
    #'AU',
    #'CN',
    #'NL',
    #'EDU',
    #'CH',
    #'ID',
    #'AT',
    #'KR',
    #'CZ',
    #'MX',
    #'BE',
    #'SE',
    #'TR',
    #'TW',
    #'AL',
    #'UA',
    #'IR',
    #'VN',
    #'CL',
    #'SK',
    #'LY',
    #'TO',
    #'NO',
    #'FI',
    #'PT'
]

# Read the word list
with open("uniquewords_english.json", 'r') as f:
    wl_dict = json.loads(f.read())
print ('Read wordlist')

# single word domains
print ('Calculating single word domains')
for w in wl_dict:
    if FilterDomain(w, '', ''):
        w1 = w.replace(' ', '')
        pdoms[w1] = []     # all single words should be added
    for s in wl_dict[w]:
        ss = s.replace(' ', '')  # some synonyms have spaces in them
        if FilterDomain(ss, '', ''):
            pdoms[ss] = []

print ('Calculating double word domains')
# two word domains whose length is less than 17 characters
for x in wl_dict:
    for y in wl_dict[x]:
        w1 = x.replace(' ', '')
        w2 = y.replace(' ', '')
        if FilterDomain(w1, w2, ''):
            pdoms[w1 + w2] = []
            pdoms[w1 + '-' + w2] = []

print ('Calculating triple word domains')
# three word domains whose length is less than 17 characters
for x in wl_dict:
    for y in wl_dict[x]:
        for z in wl_dict[x]:
            w1 = x.replace(' ', '')
            w2 = y.replace(' ', '')
            w3 = z.replace(' ', '')
            if FilterDomain(w1, w2, w3):
                pdoms[w1 + w2 + w3] =  []
                pdoms[w1 + '-' + w2 + '-' + w3] = []

for t in TLDS:
    print('Starting to calculate', t)
    domains = {}    # reset it for every tld; keep files smaller
    domains['HEADER'] = ['ZoneCheckDate', 'ZoneCheckResults', 'PingCheckDate', 'PingCheckResults', 'WhoisCheckDate',\
                         'Registrar', 'CreateDate', 'UpdateDate', 'ExprDate', 'Country']

    czds = readczds(t)  # try to read the zones if they exist

    for d in pdoms:
        z = str(d)
        x = str(t).lower()
        domain = z + '.' + x
        ZoneCheckDate = date.today().strftime('%Y-%m-%d')
        ZoneCheckResults = domain in czds
        if len(domain) > 0:
            domains[domain] = [ZoneCheckDate, ZoneCheckResults, '', '', '', '', '', '', '', '']
        else:
            domains[domain] = ['', '', '', '', '', '', '', '', '', '']

    fn = x + '.dict'
    with open(fn, 'w') as f:
        f.write(json.dumps(domains))
    print('Wrote TLD', t)



