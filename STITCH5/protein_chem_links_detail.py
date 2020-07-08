import json
with open('unzip/9606.protein_chemical.links.detailed.v5.0.tsv') as r:
    content = {}
    line = r.readline()
    content['chemical'] = [['protein' ,'experimental', 'prediction', 'database', 'textmining', 'combined_score']]
    line = r.readline()
    while line:
        split = line.split()
        if(split[0] not in content.keys()):
            content[split[0]] = []
        content[split[0]].append([split[1], split[2], split[3], split[4], split[5], split[6]])
            
        line = r.readline()
    with open('json/protein_chem_links_detailed.json','w') as f: 
        json.dump(content, f, indent=4)