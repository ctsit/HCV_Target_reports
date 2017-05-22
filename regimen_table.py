from jinja2 import Template
import json

delta_path = './regimen_table.template'

with open(delta_path, 'r') as tfile:
    dtemp = Template(tfile.read())

with open('sub_stats.json', 'r') as datafile:
    data = json.loads(datafile.read())

rows = []

for subid, subj in data.items():
    row = []
    row.append(subj['research_id'])

    row.append(subj.get('regimen'))
    row.append(subj.get('duration'))
    row.append(subj.get('cirr_status'))

    rows.append(','.join([str(item) for item in row]))

with open('regimen_report.csv', 'w') as outfile:
    outfile.write(dtemp.render({'rows':rows}))
