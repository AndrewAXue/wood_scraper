import smtplib, ssl
import requests
from bs4 import BeautifulSoup
import time
from random import randint
from datetime import datetime
import string

from collections import OrderedDict

port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = "zhangyuqi8rankin@gmail.com"
password = "Alex2001*"
TARGET = 'andrew.a.xue@gmail.com'
WAIT_MINS_BETWEEN_SCRAPES = 30
SEARCH_RADIUS_IN_KILOS = 40
KIJIJI_URLS = [
        f'https://www.kijiji.ca/b-mississauga-peel-region/firewood/k0l1700276?rb=true&ll=43.569300%2C-79.606550&address=2153+Autumn+Breeze+Dr+N%2C+Mississauga%2C+ON+L5B+1R3%2C+Canada&radius={SEARCH_RADIUS_IN_KILOS}.0&dc=true',
        f'https://www.kijiji.ca/b-mississauga-peel-region/log/k0l1700276?rb=true&ll=43.569300%2C-79.606550&address=2153+Autumn+Breeze+Dr+N%2C+Mississauga%2C+ON+L5B+1R3%2C+Canada&radius={SEARCH_RADIUS_IN_KILOS}.0&dc=true',
        f'https://www.kijiji.ca/b-mississauga-peel-region/tree/k0l1700276?rb=true&ll=43.569300%2C-79.606550&address=2153+Autumn+Breeze+Dr+N%2C+Mississauga%2C+ON+L5B+1R3%2C+Canada&radius={SEARCH_RADIUS_IN_KILOS}.0&dc=true',
        f'https://www.kijiji.ca/b-mississauga-peel-region/fire-wood/k0l1700276?rb=true&ll=43.569300%2C-79.606550&address=2153+Autumn+Breeze+Dr+N%2C+Mississauga%2C+ON+L5B+1R3%2C+Canada&radius={SEARCH_RADIUS_IN_KILOS}.0&dc=true',
        f'https://www.kijiji.ca/b-mississauga-peel-region/stump/k0l1700276?rb=true&ll=43.569300%2C-79.606550&address=2153+Autumn+Breeze+Dr+N%2C+Mississauga%2C+ON+L5B+1R3%2C+Canada&radius={SEARCH_RADIUS_IN_KILOS}.0&dc=true',
        f'https://www.kijiji.ca/b-free-stuff/mississauga-peel-region/firewood/k0c17220001l1700276?rb=true&ll=43.569300%2C-79.606550&address=2153+Autumn+Breeze+Dr+N%2C+Mississauga%2C+ON+L5B+1R3%2C+Canada&radius={SEARCH_RADIUS_IN_KILOS}.0',
        f'https://www.kijiji.ca/b-free-stuff/mississauga-peel-region/log/k0c17220001l1700276?rb=true&ll=43.569300%2C-79.606550&address=2153+Autumn+Breeze+Dr+N%2C+Mississauga%2C+ON+L5B+1R3%2C+Canada&radius={SEARCH_RADIUS_IN_KILOS}.0',
        f'https://www.kijiji.ca/b-free-stuff/mississauga-peel-region/tree/k0c17220001l1700276?radius={SEARCH_RADIUS_IN_KILOS}.0&address=2153+Autumn+Breeze+Dr+N%2C+Mississauga%2C+ON+L5B+1R3%2C+Canada&ll=43.569300,-79.606550',
        f'https://www.kijiji.ca/b-free-stuff/mississauga-peel-region/fire-wood/k0c17220001l1700276?radius={SEARCH_RADIUS_IN_KILOS}.0&address=2153+Autumn+Breeze+Dr+N%2C+Mississauga%2C+ON+L5B+1R3%2C+Canada&ll=43.569300,-79.606550',
        f'https://www.kijiji.ca/b-free-stuff/mississauga-peel-region/stump/k0c17220001l1700276?radius={SEARCH_RADIUS_IN_KILOS}.0&address=2153+Autumn+Breeze+Dr+N%2C+Mississauga%2C+ON+L5B+1R3%2C+Canada&ll=43.569300,-79.606550'
    ]
FACEBOOK_URLS = [
    'https://www.facebook.com/marketplace/search?daysSinceListed=1&query=firewood&exact=false',
    #'https://www.facebook.com/marketplace/106262189412553/search?daysSinceListed=1&query=log&exact=false',
    #'https://www.facebook.com/marketplace/106262189412553/search?daysSinceListed=1&query=tree&exact=false',
    #'https://www.facebook.com/marketplace/106262189412553/search?daysSinceListed=1&query=fire%20wood&exact=false'
]
CRAIGSLIST_URLS = [
    'https://sfbay.craigslist.org/d/for-sale/search/sss?postal=94085&query=firewood&search_distance=15&sort=rel',
    'https://sfbay.craigslist.org/d/for-sale/search/sss?postal=94085&query=log&search_distance=15&sort=rel',
    'https://sfbay.craigslist.org/d/for-sale/search/sss?postal=94085&query=tree&search_distance=15&sort=rel',
    'https://sfbay.craigslist.org/d/for-sale/search/sss?postal=94085&query=fire%20wood&search_distance=15&sort=rel',
    'https://sfbay.craigslist.org/d/for-sale/search/sss?postal=94085&query=stump&search_distance=15&sort=rel'
    'https://sfbay.craigslist.org/d/for-sale/search/sss?postal=94110&query=firewood&search_distance=15&sort=rel',
    'https://sfbay.craigslist.org/d/for-sale/search/sss?postal=94110&query=log&search_distance=15&sort=rel',
    'https://sfbay.craigslist.org/d/for-sale/search/sss?postal=94110&query=tree&search_distance=15&sort=rel',
    'https://sfbay.craigslist.org/d/for-sale/search/sss?postal=94110&query=fire%20wood&search_distance=15&sort=rel',
    'https://sfbay.craigslist.org/d/for-sale/search/sss?postal=94110&query=stump&search_distance=15&sort=rel'
]
TITLE_BLACKLIST = ['$', 'christmas', 'chainsaw', 'chain saw', 'soap', 'holder', ' art', 'art ', 'care', 'maint', 'sale', 'service', ' door', 'door ', 'decor']
DESC_BLACKLIST = ['$', 'dollar', 'christmas', 'care', 'maint', 'sale', 'service']


class FixedSizeArray:
    def __init__(self, size):
        self.cache = OrderedDict()
        with open('wood_ids.txt') as f:
            for wood_id in list(map(lambda x: x.strip(), f.readlines())):
                self.cache[wood_id] = 0
                self.cache.move_to_end(wood_id)
        self.size = size

    def __contains__(self, x):
        if x not in self.cache:
            return False
        else:
            self.cache.move_to_end(x)
            return True

    def append(self, x) -> None:
        self.cache[x] = 0
        self.cache.move_to_end(x)
        if len(self.cache) > self.size:
            self.cache.popitem(last=False)

    def save(self):
        with open('wood_ids.txt', 'w') as f:
            f.write('\n'.join(self.cache))

seen_ids = FixedSizeArray(2000)

class Ad:
    def __init__(self, ad_html):
        self.ad_html = ad_html
        self.printable = set(string.printable)

    def summary(self):
        return f'''
            Title: {self.title}
            Desc: {self.desc}
            Url: {self.link}
            Price: {self.price}

            '''

    def filter_printable(self, s):
        return ''.join(filter(lambda x: x in self.printable, s))

class KijijiAd(Ad):
    def __init__(self, ad_html):
        super(KijijiAd, self).__init__(ad_html)
        self.title = self.filter_printable(self.ad_html.find("div", {"class": "title"}).a.text.strip().lower())
        self.desc = self.filter_printable(" ".join(self.ad_html.find("div", {"class": "description"}).text.lower().split()))
        self.link = 'https:/www.kijiji.ca' + self.ad_html.find("div", {"class": "title"}).a['href']
        self.id = self.ad_html['data-listing-id']
        self.price = self.ad_html.find("div", {"class": "price"}).text.strip()

class FacebookAd(Ad):
    def __init__(self, ad_html):
        super(FacebookAd, self).__init__(ad_html)
        self.title = self.filter_printable(self.ad_html.find("div", {"class": "title"}).a.text.strip().lower())
        self.desc = self.filter_printable(" ".join(self.ad_html.find("div", {"class": "description"}).text.lower().split()))
        self.link = 'https:/www.kijiji.ca' + self.ad_html.find("div", {"class": "title"}).a['href']
        self.id = self.ad_html['data-listing-id']
        self.price = self.ad_html.find("div", {"class": "price"}).text.strip()

class CraiglistAd(Ad):
    def __init__(self, ad_html):
        super(CraiglistAd, self).__init__(ad_html)
        self.title = self.filter_printable(self.ad_html.find('a', {'class': 'result-title'}).text.strip().lower())
        self.desc = 'wood'
        self.link = self.ad_html.find('a', {'class': 'result-title'})['href']
        self.id = self.ad_html['data-pid']
        price_span = self.ad_html.find('span', {'class': 'result-price'})
        if price_span:
            self.price = price_span.text
        else:
            self.price = '0'

def send_email(message):
    message = message

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, TARGET, message)

def good_ad(ad, seen_ids):
    if ad.id in seen_ids:
        return False
    if '$' in ad.price:
        return False
    for title_black in TITLE_BLACKLIST:
        if title_black in ad.title:
            return False
    for desc_black in DESC_BLACKLIST:
        if desc_black in ad.desc:
            return False
    return True

def retry_get(url, tries):
    for _ in range(tries):
        try:
            data = requests.get(url)
            return data
        except:
            pass
    print(f'failed getting URL {url} {tries} times')
    exit(1)


def query_url(url, ad_class, seen_ids, ad_html_class):
    data = retry_get(url, 3)
    if data.status_code != 200:
        print(f'Url {url} gave non 200 status code')
        return ''
    soup = BeautifulSoup(data.text, 'html.parser')
    ads = list(map(lambda x: ad_class(x), soup.find_all("article", {"class": ad_html_class}))) + \
          list(map(lambda x: ad_class(x), soup.find_all("div", {"class": ad_html_class}))) + \
          list(map(lambda x: ad_class(x), soup.find_all("li", {"class": ad_html_class})))
    email_msg = ''
    if len(ads) == 0:
        print(f'Url {url} did not have any ads')
        return ''
    for ad in ads:
        if good_ad(ad, seen_ids):
            seen_ids.append(ad.id)
            email_msg += ad.summary()
        elif ad.id not in seen_ids and '$' not in ad.price:
            print(f'''
            Filtered out ad ======================================
            {ad.summary()}
            ======================================================

            ''', flush=True)
    return email_msg

def query_urls():
    composite_email_msg = ''
    #for url in KIJIJI_URLS:
    #    time.sleep(randint(10, 40))
    #    composite_email_msg += query_url(url, KijijiAd, seen_ids, "search-item regular-ad")
    #for url in FACEBOOK_URLS:
    #    time.sleep(randint(10, 40))
    #    composite_email_msg += query_url(url, FacebookAd, seen_ids, "b3onmgus ph5uu5jm g5gj957u buofh1pr cbu4d94t rj1gh0hx j83agx80 rq0escxv fnqts5cd fo9g3nie n1dktuyu e5nlhep0 ecm0bbzt")
    for url in CRAIGSLIST_URLS:
        time.sleep(randint(10, 40))
        composite_email_msg += query_url(url, CraiglistAd, seen_ids, "result-row")

    if composite_email_msg:
        composite_email_msg = '''
            Get WOOD POSTED BITCH
            
        ''' + composite_email_msg
        print(composite_email_msg, flush=True)
        send_email(composite_email_msg.encode())
    else:
        print('No new ads found', flush=True)
    seen_ids.save()

print('Starting...', flush=True)
print(f'Sending wood posts to {TARGET}', flush=True)
while True:
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f"Starting scrape at = {current_time}", flush=True)
    query_urls()

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Finished run at =", current_time, flush=True)
    time.sleep(WAIT_MINS_BETWEEN_SCRAPES * 60 + 60 * randint(-5, 5))
