import json
with open('unzip/9606.actions.v5.0.tsv') as r:
    
    content = {}
    line = r.readline()
    content['action_list'] = [['item_id_a' ,'item_id_b', 'mode', 'action', 'a_is_acting', 'score']]
    line = r.readline()
    while line:
        split = line.split()
        if(len(split) == 6):
            content['action_list'].append([split[0], split[1], split[2], split[3], split[4], split[5]])
        else:
            content['action_list'].append([split[0], split[1], split[2], '', split[3], split[4]])           
            
        line = r.readline()
    with open('json/actions.json','w') as f: 
        json.dump(content, f, indent=4)