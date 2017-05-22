import csv
import json
import yaml
from cappy import API
from copy import copy

with open('./settings.yaml', 'r') as settings_file:
    settings = yaml.load(settings_file)
    token = settings['token']
    rurl = settings['redcap_url']

api = API(token, rurl, 'lineman.json')

# records = api.export_records(fields=['dm_subjid', 'dm_usubjid', 'reg_oth_suppcm_regimen', 'dis_dsstdy'], forms=['chemistry_imported', 'inr_imported', 'early_discontinuation_eot']).content
records = api.export_records(fields=['dm_subjid', 'dm_usubjid'], forms=['cirrhosis', 'chemistry_imported', 'inr_imported', 'early_discontinuation_eot', 'treatment_regimen', 'derived_values_baseline']).content
with open('local.records.json', 'w') as outfile:
    outfile.write(str(records, 'utf-8'))
records = json.loads(str(records, 'utf-8'))

def get_end_date(eot):
    ymd = [int(num) for num in eot.split('-')]
    ymd[1] += 9
    if ymd[1] > 12:
        ymd[0] += 1
        ymd[1] -= 12
    return '-'.join([str(s) for s in ymd])

acc = {}
has_eot_list = []
eot = 'eot_dsstdtc'
subjs = list(set([item['dm_subjid'] for item in records]))
for subj in subjs:
    eot = None
    research_id = None
    for record in records:
        if record.get('eot_dsstdtc'):
            eot = record.get('eot_dsstdtc')
        if record.get('reg_oth_suppcm_regimen'):
            regimen = record.get('reg_oth_suppcm_regimen')
        if record.get('dis_dsstdy'):
            duration = record.get('dis_dsstdy')
        if record.get('cirr_suppfa_cirrstat'):
            cirr_status = record.get('cirr_suppfa_cirrstat')
    if eot:
        has_eot_list.append((subj, eot))

for subj, eot in has_eot_list:
    acc[subj] = {
        'records': [],
        'eot': eot,
        'regimen': regimen,
        'duration': duration,
        'cirr_status': cirr_status,
        'end_date': get_end_date(eot),
        'baseline': {}
    }

def clean_record(record):
    mutable = copy(record)

    for key, val in zip(record.keys(), record.values()):
        if not val:
            del mutable[key]

    return mutable

for key in acc.keys():
    for record in records:
        if record.get('dm_subjid') == key:
            acc[key]['records'].append(clean_record(record))

for key in acc.keys():
    records = acc[key]['records']
    for record in records:
        if record.get('dm_usubjid'):
            acc[key]['research_id'] = record.get('dm_usubjid')

with open('new_records.json', 'w') as outfile:
    outfile.write(json.dumps(acc, indent=4))

