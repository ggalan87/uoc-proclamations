from bs4 import BeautifulSoup
from requests_html import HTMLSession
import pickle

from models import *

base_url = 'http://proclamations.edu.uoc.gr'
page_suffix = '?pg='

proclamations = []
proclamations_raw = []

page_number = 18

continue_scraping = True

while continue_scraping:
    print('Extracting from page {}'.format(page_number))

    # if session is put outside, then we get an error after few connections
    session = HTMLSession()
    r = session.get(base_url + page_suffix + str(page_number))

    if r.status_code != 200:
        break

    r.html.render()
    table = r.html.find('#results', first=True)

    soup = BeautifulSoup(table.html, 'html.parser')
    table_rows = soup.find_all('tr')
    table_rows = table_rows[1:]  # Discard header

    for i, row in enumerate(table_rows):
        cols = row.find_all('td')
        proc = Proclamation(cols, base_url)

        if '2019' in proc.competition_date or \
                '2019' in proc.publication_date or \
                '2019' in proc.proclamation_date or \
                '2019' in proc.submission_deadline:
            pass
        else:
            print(proc)
            continue_scraping = False
            break

        proclamations.append(proc)


    page_number += 1


pickle.dump(proclamations, open('proclamations.pkl', 'wb'))