import json
from copy import copy

with open('new_records.json', 'r') as datafile:
    data = json.loads(datafile.read())

for subid, subj in zip(data.keys(), data.values()):
    for rec in subj['records']:
        keys = list(rec.keys())

        if not ( 'eot_dsstdtc' in keys or 'chem_im_lbdtc' in keys or 'inr_im_lbdtc' in keys ):
            rec['delete_me'] = True

    subj['records'] = [record for record in subj['records'] if not record.get('delete_me')]

with open('cleared_records.json', 'w') as outfile:
    outfile.write(json.dumps(data, indent=4))


