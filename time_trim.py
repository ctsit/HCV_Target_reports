import json
from copy import copy

with open('redi_records.json', 'r') as datafile:
    data = json.loads(datafile.read())

mutable = copy(data)
for subj in mutable.values():
    del subj['baseline']
closest_by_subj_chem = {}
closest_by_subj_inr = {}

def clean_records(mutable, data, closest, form, date_field):
    for subid, subj in data.items():
        end = subj['end_date']
        eot = subj['eot']
        for index, record in enumerate(subj[form]):
            record_date = record.get(date_field)
            if not record_date:
                record_date = '9999-99-99' # always greater than any end date

            # get rid of records outside the range
            if record_date > end:
                mutable[subid][form][index]['_status'] = 'after_36weeks'

            # delete all records before the eot date
            elif record_date <= eot:
                mutable[subid][form][index]['_status'] = 'before_eot'
                # but make sure we are keeping the closest to eot around
                if not closest.get(subid):
                    closest[subid] = {
                        'date': record_date,
                        'val': record
                    }
                elif record_date > closest[subid]['date']:
                    closest[subid] = {
                        'date': record_date,
                        'val': record
                    }
                else:
                    pass

            # do nothing to the mutable structure when the record is in the range
            elif record_date >= eot and record_date <= end:
                mutable[subid][form][index]['_status'] = 'in_range'

            # in case something bad / weird happens we know
            else:
                print(subid)
                print('has a record with bad data')
                print(record)
                exit()

clean_records(mutable, data, closest_by_subj_chem, 'chem', 'chem_im_lbdtc')
clean_records(mutable, data, closest_by_subj_inr, 'inr', 'inr_im_lbdtc')

# set the baseline to be the closest record by subject
def set_baseline(mutable, closest, form):
    for subid in closest.keys():
        mutable[subid]['baseline_{}'.format(form)] = closest[subid]['val']

set_baseline(mutable, closest_by_subj_chem, 'chem')
set_baseline(mutable, closest_by_subj_inr, 'inr')

with open('time_status.json', 'w') as outfile:
    outfile.write(json.dumps(mutable, indent=4, sort_keys=True))

report = {}
def build_report(mutable, report, form):
    base_recs = 'subjects_with_baseline_{}'.format(form)
    base_recs_count = '_subjects_with_baseline_{}_count'.format(form)
    in_range_recs = 'subjects_with_in_range_records_{}'.format(form)
    in_range_recs_count = '_subjects_with_in_range_recs_{}_count'.format(form)
    has_both = 'has_both_{}'.format(form)
    has_both_count = '_has_both_{}_count'.format(form)
    report[base_recs] = []
    report[in_range_recs] = []
    report[has_both] = []

    for subid, subj in mutable.items():
        subj[form] = [rec for rec in subj[form] if rec.get('_status') == 'in_range']
        rec_num = len(subj[form])
        has_base = len(list((subj.get('baseline_{}'.format(form)) or {}).keys()))

        if rec_num:
            report[in_range_recs].append(subid)

        if has_base:
            report[base_recs].append(subid)

        if subid in report[base_recs] and subid in report[in_range_recs]:
            report[has_both].append(subid)

    report[in_range_recs_count] = len(set(report[in_range_recs]))
    report[base_recs_count] = len(set(report[base_recs]))
    report[has_both_count] = len(set(report[has_both]))

build_report(mutable, report, 'chem')
build_report(mutable, report, 'inr')

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
    outfile.write(json.dumps(report, indent=4, sort_keys=True))
