#%%
import time
import re
import os
import bs4 
import json
import requests
from pandas import read_html
from requests.exceptions import ConnectionError
from tqdm import tqdm
from pprint import pprint
# from functools import reduce
#%%

url = lambda link : f'http://bioinformatics.charite.de/transformer{link}'

index = '/index.php?site=drug_search'
drug_page = bs4.BeautifulSoup(requests.get(url(index)).content, 'lxml')

for li in drug_page.find_all('li'):
    unit_list = []
    drug_dict = {}
    try:
        link = li.find('a', 'atc_link')['href'][1:]
        content_page = bs4.BeautifulSoup(requests.get(url(link)).content, 'lxml')
        table = content_page.find('table', attrs={"width": "90%"})
        #print(table)
        
        for tr in table.find_all('tr'):
            num = 0
            for td in tr.find_all('td'):
                br = str(td).replace('<br/>', '\n')
                unit_list.append(re.sub(u"\\<.*?\\>", " ", br).strip())
        #print(unit_list)
        drug_dict[unit_list[1]] = {}
        
        for idx in range(2, len(unit_list)):
            if(unit_list[idx] == 'CYP interactions'):
                break
            if(idx % 2 == 0):
                drug_dict[unit_list[1]][unit_list[idx].replace('\n', ' ')] = unit_list[idx + 1].split('\n')
            idx += 2
            
        print(unit_list[1])
        
        with open('drug_json/' + str(unit_list[1]) + '.json', 'w') as f:
            json.dump(drug_dict, f, indent=5)
            
            
        #break
    except TypeError:
        continue
    

