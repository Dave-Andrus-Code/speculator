
import whois, os, json
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
    'ORG',
    'XYX',
    'IO',
    'ME',
    'INFO',
    'IN',
    'TOP',
    'EU',
    'AI',
    'ONLINE',
    'US',
    'BIZ',
    'GG',
    'TECH',
    'TV',
    'CC',
    'DEV',
    'CLUB',
    'APP',
    'PW',
    'PRO',
    'SITE',
    'CA',
    'SHOP',
    'UK',
    'CO.UK',
    'WIN',
    'STORE',
    'SPACE',
    'ES',
    'IT',
    'WORK',
    'CLOUD',
    'LIVE',
    'WS',
    'RU',
    'IM',
    'ONE',
    'LIFE',
    'LINK',
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
    if file[-9:] == 'exdb.json':
        with open(file, 'r') as f:
            data = json.loads(f.read())

        for domain in data:
            # reset everything
            dcounter += 1
            check_date = date.today().strftime('%Y-%m-%d')
            registrar = ''
            creation_date = ''
            updated_date = ''
            expiration_date = ''
            country = ''

            skip_domain = ''

            try:
                if data[domain][3] != '':
                    skip_domain = True
                    dexp = datetime.strptime(data[domain][3], "%Y-%m-%d")
            except IndexError as ie:
                # The index doesn't exist -- it has never been checked
                skip_domain = False
                dexp = ''
            except Exception as e:
                print(domain, e, type(e))



            if not skip_domain:
                try:
                    # happy path, if WHOIS returns a domain that is registered
                    w = whois.whois(domain)
                    if w.domain_name == 'None' or not w.domain_name:
                        # do nothing yet
                        pass
                    else:
                        registrar = last(w.registrar)
                        creation_date = last(w.creation_date)
                        updated_date = last(w.updated_date)
                        expiration_date = last(w.expiration_date)
                        country = last(w.country)
                except:
                    # if a domain is not registered, just move on
                    pass

                data[domain] = [check_date,\
                                registrar,\
                                creation_date,\
                                expiration_date,\
                                w.emails,\
                                country]
                print (data[domain])
                if dcounter > 30:
                    print('Writing', file, domain)
                    with open(file, 'w') as f:
                        f.write(json.dumps(data))
                    dcounter = 0
