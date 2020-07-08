import json
with open('unzip/9606.protein_chemical.links.transfer.v5.0.tsv') as r:
    
    content = {}
    line = r.readline()
    content['chemical'] = [['protein' ,'experimental_direct', 'experimental_transferred', 'prediction_direct', 
                            'prediction_transferred', 'database_direct', 'database_transferred', 'textmining_direct', 
                            'textmining_transferred', 'combined_score']]
    line = r.readline()
    while line:
        split = line.split()
        if(split[0] not in content.keys()):
            content[split[0]] = []
        content[split[0]].append([split[1], split[2], split[3], split[4], split[5], split[6],
                                  split[7], split[8], split[9], split[10]])
            
        line = r.readline()
    with open('json/protein_chem_links_transfer.json','w') as f: 
        json.dump(content, f, indent=4)
    