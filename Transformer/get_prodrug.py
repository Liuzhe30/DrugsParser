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

url = lambda link : f'http://bioinformatics.charite.de/transformer{link}'

index = '/index.php?site=prodrug_search'
drug_page = bs4.BeautifulSoup(requests.get(url(index)).content, 'lxml')
for li in drug_page.find_all('li'):
    unit_list = []
    drug_dict = {}
    try:
        link = li.find('a', 'atc_link')['href'][1:]
        content_page = bs4.BeautifulSoup(requests.get(url(link)).content, 'lxml')
        table = content_page.find('div', attrs={'id': "contentwrapper"})
        #print(table)
        
        try:
            for tr in table.find_all('tr'):
                for td in tr.find_all('td'):
                    br = str(td).replace('<br/>', '\n')
                    unit_list.append(re.sub(u"\\<.*?\\>", " ", br).strip())
            new_list = unit_list[1:]
            #print(new_list)
            drug_dict[new_list[1]] = {}
            
            for idx in range(2, len(new_list)):
                if(new_list[idx] == 'CYP interactions' or new_list[idx] == 'Phase2 interactions'):
                    break
                if(idx % 2 == 0):
                    drug_dict[new_list[1]][new_list[idx].replace('\n', ' ')] = new_list[idx + 1].split('\n')
                if(new_list[idx] == 'H-Bond Acceptors'):
                    break
                idx += 2
                
              
            #pprint(drug_dict)  
            print(new_list[1])
            
            with open('prodrug_json/' + str(new_list[1]) + '.json', 'w') as f:
                json.dump(drug_dict, f, indent=5)
                
        except (AttributeError, FileNotFoundError, IndexError):
            continue
                
        #break
    except TypeError:
        continue


