
import os, json
import dns, dns.resolver
from datetime import date
from datetime import datetime

def last(arg):
    # returns the last element in a list or the value of the string passed

    # if this is a list, pick the last item in the list
    if isinstance(arg, list):
        arg = arg[len(arg)-1]

    # try converting the arg to a date
    try:
        x = date.strftime(arg, '%Y-%m-%d')
        return x
    except:
        # it's not a date, nothing to do
        pass

    return(arg)

# The top TLD's based on indexed pages and registrations
TLD = [
    'COM',
    'NET',
    'CO',
    'ORG',  #
    'XYX',
    'IO',  # N/A
    'ME',  # N/A
    'INFO',  #
    'IN',  # N/A
    'TOP',
    'EU',  #N/A
    'AI',  #NA
    'ONLINE',  #
    'US',  #NA
    'BIZ',
    'GG',  #NA
    'TECH',  #
    'TV',  #NA
    'CC',  #NA
    'DEV',  #
    'CLUB',
    'APP',  #
    'PW',
    'PRO',  #
    'SITE',  #
    'CA',  #NA
    'SHOP',
    'UK',
    'CO.UK',
    'WIN',  #NA
    'STORE',  #
    'SPACE',  #
    'DOWNLOAD',  #
    'ES',
    'IT',
    'WORK',
    'CLOUD',
    'LIVE',  #
    'WS',
    'RU',
    'IM',
    'ONE',
    'LIFE',  #
    'LINK',  #
    'JP',
    'DE',
    'FR',
    'BR',
    'GOV',
    'PL',
    'AU',
    'CN',
    'NL',
    'EDU',
    'CH',
    'ID',
    'AT',
    'KR',
    'CZ',
    'MX',
    'BE',
    'SE',
    'TR',
    'TW',
    'AL',
    'UA',
    'IR',
    'VN',
    'CL',
    'SK',
    'LY',
    'TO',
    'NO',
    'FI',
    'PT'
]

data = {}
dcounter = 0

# Read the word list temp (WLT) files and build the dictionary.
for file in os.listdir():
    if file[-5:] == '.dict':
        with open(file, 'r') as f:
            data = json.loads(f.read())

        for domain in data:
            # get the current status of the ping check
            zcd = data[domain][0]
            zcr = data[domain][1]
            chkdt = data[domain][2]
            chkres = data[domain][3]

            # Can we skip a domain in the CZDS?
            skip_domain = True
            if zcd == '' or not zcr:
                skip_domain = False
            else:
                # Have we done a ping test recently
                if chkdt == 'PingCheckDate' or chkres == 'PingCheckResults':
                    # just for old data files; we shouldn't see this anymore
                    skip_domain = False
                else:
                    # If the old values don't exist, check if new values do
                    if chkdt == '' or chkres == '':
                        skip_domain = False
                    else:
                        skip_domain = True

            # Get the ping results
            if not skip_domain:
                print('Checking', domain)
                dcounter += 1
                chkdt = date.today().strftime('%Y-%m-%d')
                try:
                    chk = dns.resolver.resolve(domain, 'A')
                    if len(chk) > 0:
                        chkres = True
                except:
                    chkres = False
            else:
                print('Skipping', domain)

                # store the results in memory
                data[domain] = [zcd, zcr, chkdt, chkres, data[domain][4], data[domain][5], data[domain][6], \
                                data[domain][7], data[domain][8], data[domain][9]]

                # write to disk is we've checked a bunch
                if dcounter > 100:
                    print('Writing', file, domain)
                    with open(file, 'w') as f:
                        f.write(json.dumps(data))
                    dcounter = 0
                    print ('Done writing.')


