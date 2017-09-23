#!/usr/bin/env python
# -*- coding: utf-8 -*
import requests  # requests
from bs4 import BeautifulSoup  # bs4 BeautifulSoup
import os
import csv

def request(url):
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) \
     AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
    content = requests.get(url, headers=headers)
    return content

def scrapcourse(url):
    content = request(url)
    soup = BeautifulSoup(content.text,'lxml')
    all_c = soup.find('div',id='sc_sccoursedescs').find_all('div', class_='courseblock')
    with open('tamucourseug.csv', 'a',encoding='utf-8') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='"', lineterminator='\n')
        for c in all_c:
            title = c.find('p',class_= "courseblocktitle noindent").find('strong').get_text()
            dep = title[:4]
            no = title[5:8]
            if title[8:9] == '/':
                name = title[18:]
            else:
                name = title[9:]
            name = name.strip()
            credit = c.find('p',class_="hours noindent").find('strong').get_text()
            credit = int(credit[credit.find('.')-1])
            desc = c.find('p',class_="courseblockdesc").get_text().strip()
            spamwriter.writerow([dep] + [no] + [name] + [str(credit)] + [desc])

with open('tamucourseug.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', lineterminator='\n')
    spamwriter.writerow(['Department']  + ['NO'] + ['Name'] + ['Credit'] + ['Description'])


main_url = "http://catalog.tamu.edu/undergraduate/course-descriptions/"
cont = request(main_url)
soup = BeautifulSoup(cont.text,'lxml')
all_u = soup.find('div',id='atozindex').find_all('a')
for u in all_u:
    href = u['href']
    s_url = 'http://catalog.tamu.edu' + href
    scrapcourse(s_url)


