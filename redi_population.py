import json
from copy import copy

with open('cleared_records.json', 'r') as infile:
    data = json.loads(infile.read())

redi = {}
notredi = {}

for subid, subj in data.items():
    records = subj['records']

    if len(records) > 1:
        redi[subid] = subj
    elif len(records) == 1:
        if records[0]['chemistry_imported_complete'] != '0' or records[0]['inr_imported_complete'] != '0':
            redi[subid] = subj
        else:
            notredi[subid] = subj
    else:
        notredi[subid] = subj


for subid, subj in data.items():
    records = subj['records']
    subj['inr'] = [copy( record ) for record in records]
    for record in subj['inr']:
        keys = list(record.keys())
        for key in keys:
            if not 'inr' in key:
                del record[key]
    for record in records:
        keys = list(record.keys())
        for key in keys:
            if 'inr' in key:
                del record[key]
    subj['chem'] = copy(records)
    del subj['records']


rkeys = len(set(list(redi.keys())))
nkeys = len(set(list(notredi.keys())))

with open('redi_records.json', 'w') as outfile:
    outfile.write(json.dumps(redi, indent=4, sort_keys=True))

with open('notredi_records.json', 'w') as outfile:
    outfile.write(json.dumps(notredi, indent=4, sort_keys=True))

with open('records_stats.json', 'w') as outfile:
    outfile.write(json.dumps({
        'redi_eot_subj_count': rkeys,
        'not_redi_eot_subj_count': nkeys,
    }, indent=4, sort_keys=True))
