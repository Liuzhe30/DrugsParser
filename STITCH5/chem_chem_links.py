import json
with open('unzip/chemical_chemical.links.v5.0.tsv') as r:
    content = {}
    line = r.readline()
    content['chemical1'] = [['chemical2' ,'textmining']]
    line = r.readline()
    while line:
        split = line.split()
        if(split[0] not in content.keys()):
            content[split[0]] = []
        content[split[0]].append([split[1], split[2]])
            
        line = r.readline()
    with open('json/chem_chem_links.json','w') as f: 
        json.dump(content, f, indent=4)