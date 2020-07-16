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
            drug_dict[new_list[1]] = {}
            
            print(new_list[1])
            
            for line in str(content_page).split('\n'): # <table style="table-layout:fixed;" align=center class="result">
                #print(line)
                if('Mechanism of Activation' in line):
                    #print(line)
                    line = re.sub(u"\\<.*?\\>", "|", line).strip()
                    list = line.split('|')
                    while '' in list:
                        list.remove('')       
                    drug_dict[new_list[1]]['name'] = new_list[1]
                    
                    if(len(list) == 7):
                        drug_dict[new_list[1]]['Prodrug'] = list[-3]
                        drug_dict[new_list[1]]['Reaction'] = list[-2]
                        drug_dict[new_list[1]]['Active drug'] = list[-1].replace(' ','Not given')
                    else:
                        drug_dict[new_list[1]]['Prodrug'] = list[-4]
                        drug_dict[new_list[1]]['Reaction'] = list[-3]
                        drug_dict[new_list[1]]['Active drug'] = list[-2].replace(' ','Not given')                        
            
            #pprint(drug_dict)          


            with open('activation_json/' + str(new_list[1]) + '.json', 'w') as f:
                json.dump(drug_dict, f, indent=5)
          
        except IndexError:
        #except (AttributeError, FileNotFoundError, IndexError):
            continue
                
        #break
    except TypeError:
        continue