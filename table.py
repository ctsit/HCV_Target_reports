from jinja2 import Template
import json

delta_path = './deltatable.template'

with open(delta_path, 'r') as tfile:
    dtemp = Template(tfile.read())

with open('sub_stats.json', 'r') as datafile:
    data = json.loads(datafile.read())

rows = []
for subid, subj in data.items():
    rid = subj['research_id']
    kv = list(subj.items())

    key_data = [key.split('_') for key in subj.keys()]
    tests = [item[1:-1] for item in key_data]
    tests = [item for item in tests if len(item) == 3]
    tests = ['_'.join(item) for item in tests]
    tests_uniq = []
    for test in tests:
        if test not in tests_uniq:
            tests_uniq.append(test)

    tests = tests_uniq

    bases = [val for key, val in kv if 'baseline' in key]

    maxes = [val for key, val in kv if 'max' in key]
    mins = [val for key, val in kv if 'min' in key]
    means = [val for key, val in kv if 'mean' in key]
    sigmas = [val for key, val in kv if 'sigma' in key]
    delta = [val for key, val in kv if 'delta' in key and not 'deltas' in key]
    rids = [rid for item in range(555)]

    row_gen = zip(rids, tests, bases, mins, maxes, means, sigmas, delta)
    for row in row_gen:
        rows.append(','.join([str(item) for item in list(row)]))

with open('delta_report.csv', 'w') as outfile:
    outfile.write(dtemp.render({'rows':rows}))
