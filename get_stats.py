import json
from copy import copy
from stat_utils import *

with open('time_trimmed.json', 'r') as infile:
    data = json.loads(infile.read())

subject_stats = {}

inr_fields = [
    'inr_im_lborres',
]
chem_fields = [
    'alt_im_lborres',
    'ast_im_lborres',
    'dbil_im_lborres',
    'tbil_im_lborres',
]

inr_date = 'inr_im_lbdtc'
chem_date = 'chem_im_lbdtc'
import pdb
for subid, subj in data.items():
    forms = ['chem', 'inr']

    for form in forms:
        fields = chem_fields if form == 'chem' else inr_fields
        date_field = chem_date if form == 'chem' else inr_date
        recs = copy(subj.get(form)) or []
        base = copy(subj.get('baseline_{}'.format(form))) or {}
        recs.insert(0, base)

        for field in fields:
            # pdb.set_trace()
            field_recs = copy([rec for rec in recs if rec.get(field)])
            delta, deltas = get_delta(field_recs, field, date_field)
            # pdb.set_trace()
            if not subject_stats.get(subid):
                subject_stats[subid] = {}
            subject_stats[subid]['{}_{}_baseline'.format(form, field)] = base.get(field)
            subject_stats[subid]['{}_{}_mean'.format(form, field)] = get_mean(field_recs, field)
            subject_stats[subid]['{}_{}_max'.format(form, field)] = get_max(field_recs, field)
            subject_stats[subid]['{}_{}_min'.format(form, field)] = get_min(field_recs, field)
            subject_stats[subid]['{}_{}_sigma'.format(form, field)] = get_std_dev(field_recs, field)
            subject_stats[subid]['{}_{}_delta'.format(form, field)] = delta
            subject_stats[subid]['{}_{}_deltas'.format(form, field)] = deltas
        subject_stats[subid]['total_{}_records'.format(form)] = len(recs)
    subject_stats[subid]['research_id'] = subj['research_id']

with open('sub_stats.json', 'w') as outfile:
    outfile.write(json.dumps(subject_stats, indent=4, sort_keys=True))
