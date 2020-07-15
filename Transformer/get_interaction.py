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

index = '/index.php?site=biotransformation'
drug_page = bs4.BeautifulSoup(requests.get(url(index)).content, 'lxml')

for li in drug_page.find_all('li'):
    unit_list = []
    drug_dict = {}
    try:
        content = li.find('a')
        link = content['href'][1:]
        if('fullinfo_results&cname' in str(link)):
            name = re.sub(u"\\<.*?\\>", "", str(content))
            content_page = bs4.BeautifulSoup(requests.get(url(link)).content, 'lxml')
            
            table = content_page.find('table', attrs={'class': "ref"})
            try:
                for tr in table.find_all('tr'):
                    for td in tr.find_all('td'):
                        br = str(td).replace('<br/>', '\n')
                        unit_list.append(re.sub(u"\\<.*?\\>", " ", br).strip())

                drug_dict[name] = {}
                for idx in range(0, len(unit_list)):
                    if(idx % 3 == 0):
                        drug_dict[name][unit_list[idx]] = {}
                        drug_dict[name][unit_list[idx]]['name'] = unit_list[idx]
                        drug_dict[name][unit_list[idx]]['Relation'] = unit_list[idx + 1].split('\n')                        
                        drug_dict[name][unit_list[idx]]['References(pubmed-id)'] = unit_list[idx + 2].replace(",", "").replace(" ", "").split('\n')  
                    idx += 3
                
                #pprint(drug_dict)    
                print(name)
                
                with open('inter_json/' + str(name) + '.json', 'w') as f:
                    json.dump(drug_dict, f, indent=5)
                  
            except (AttributeError, FileNotFoundError, IndexError):
                continue            
        
            
    except TypeError:
        continue