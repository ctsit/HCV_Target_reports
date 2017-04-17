import json
from copy import copy

with open('redi_records.json', 'r') as datafile:
    data = json.loads(datafile.read())

mutable = copy(data)
for subj in mutable.values():
    del subj['baseline']
closest_by_subj_chem = {}
closest_by_subj_inr = {}

# get rid of any records past the end date
for subid, subj in data.items():
    end = subj['end_date']
    eot = subj['eot']
    print(subid)
    for index, record in enumerate(subj['chem']):

        record_date = record.get('chem_im_lbdtc')
        if not record_date:
            record_date = '9999-99-99' # always greater than any end date

        # get rid of records outside the range
        if record_date > end:
            mutable[subid]['chem'][index]['_status'] = 'after_36weeks'

        # delete all records before the eot date
        elif record_date <= eot:
            mutable[subid]['chem'][index]['_status'] = 'before_eot'
            # but make sure we are keeping the closest to eot around
            if not closest_by_subj_chem.get(subid):
                closest_by_subj_chem[subid] = {
                    'date': record_date,
                    'val': record
                }
            elif record_date > closest_by_subj_chem[subid]['date']:
                print(eot)
                print(record_date)
                print(closest_by_subj_chem[subid]['date'])
                print()
                closest_by_subj_chem[subid] = {
                    'date': record_date,
                    'val': record
                }
            else:
                pass

        # do nothing to the mutable structure when the record is in the range
        elif record_date >= eot and record_date <= end:
            mutable[subid]['chem'][index]['_status'] = 'in_range'

        # in case something bad / weird happens we know
        else:
            print(subid)
            print('has a record with bad data')
            print(record)
            exit()

for subid, subj in data.items():
    end = subj['end_date']
    eot = subj['eot']
    print(subid)
    for index, record in enumerate(subj['inr']):

        record_date = record.get('inr_im_lbdtc')
        if not record_date:
            record_date = '9999-99-99' # always greater than any end date

        # get rid of records outside the range
        if record_date > end:
            mutable[subid]['inr'][index]['_status'] = 'after_36weeks'

        # delete all records before the eot date
        elif record_date <= eot:
            mutable[subid]['inr'][index]['_status'] = 'before_eot'
            # but make sure we are keeping the closest to eot around
            if not closest_by_subj_inr.get(subid):
                closest_by_subj_inr[subid] = {
                    'date': record_date,
                    'val': record
                }
            elif record_date > closest_by_subj_inr[subid]['date']:
                print(eot)
                print(record_date)
                print(closest_by_subj_inr[subid]['date'])
                print()
                closest_by_subj_inr[subid] = {
                    'date': record_date,
                    'val': record
                }
            else:
                pass

        # do nothing to the mutable structure when the record is in the range
        elif record_date >= eot and record_date <= end:
            mutable[subid]['inr'][index]['_status'] = 'in_range'

        # in case something bad / weird happens we know
        else:
            print(subid)
            print('has a record with bad data')
            print(record)
            exit()

# set the baseline to be the closest record by subject
for subid in closest_by_subj_chem.keys():
    mutable[subid]['baseline_chem'] = closest_by_subj_chem[subid]['val']

for subid in closest_by_subj_inr.keys():
    mutable[subid]['baseline_inr'] = closest_by_subj_inr[subid]['val']

with open('time_status.json', 'w') as outfile:
    outfile.write(json.dumps(mutable, indent=4, sort_keys=True))

has_inrange_recordsc_count = 0
has_inrange_recordsi_count = 0
has_baselinec = 0
has_baselinei = 0
has_base_and_recordsc = 0
has_base_and_recordsi = 0
for subj in mutable.values():
    subj['chem'] = [record for record in subj['chem'] if record.get('_status') == 'in_range']
    subj['inr'] = [record for record in subj['inr'] if record.get('_status') == 'in_range']
    basec_keys_len = len(list(( subj.get('baseline_chem') or {} ).keys()))
    basei_keys_len = len(list(( subj.get('baseline_inr') or {} ).keys()))
    if (len(subj['chem'])):
        has_inrange_recordsc_count += 1
    if (len(subj['inr'])):
        has_inrange_recordsi_count += 1
    if basec_keys_len:
        has_baselinec += 1
        if (len(subj['chem'])):
            has_base_and_recordsc += 1
    if basei_keys_len:
        has_baselinei += 1
        if (len(subj['inr'])):
            has_base_and_recordsi += 1

mut2 = copy(mutable)
for subid, subj in mutable.items():
    rclen = len(subj['chem'])
    rilen = len(subj['inr'])
    basec_keys_len = len(list(( subj.get('baseline_chem') or {} ).keys()))
    basei_keys_len = len(list(( subj.get('baseline_inr') or {} ).keys()))
    if ( not rclen and not rilen ) or ( not basec_keys_len and not basei_keys_len ):
        del mut2[subid]

with open('time_trimmed.json', 'w') as outfile:
    outfile.write(json.dumps(mut2, indent=4, sort_keys=True))

with open('time_trimmed_stats.json', 'w') as outfile:
    outfile.write(json.dumps({
        'has_inrange_recordsc_count': has_inrange_recordsc_count,
        'has_baselinec': has_baselinec,
        'has_base_and_recordsc': has_base_and_recordsc,
        'has_inrange_recordsi_count': has_inrange_recordsi_count,
        'has_baselinei': has_baselinei,
        'has_base_and_recordsi': has_base_and_recordsi
    }, indent=4, sort_keys=True))
