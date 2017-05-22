from jinja2 import Template
import json

delta_path = './futable.template'

with open(delta_path, 'r') as tfile:
    dtemp = Template(tfile.read())

with open('sub_stats.json', 'r') as datafile:
    data = json.loads(datafile.read())

rows = []

for subid, subj in data.items():
    row = []
    row.append(subj['research_id'])

    row.append(subj['chem_weeks_to_first_followup'])
    row.append(subj['chem_week_to_last_followup'])
    row.append(subj['chem_followup_period_weeks_length'])

    row.append(subj['inr_weeks_to_first_followup'])
    row.append(subj['inr_week_to_last_followup'])
    row.append(subj['inr_followup_period_weeks_length'])

    row.append(subj['regimen'])
    row.append(subj['duration'])

    rows.append(','.join([str(item) for item in row]))

with open('follow_up_report.csv', 'w') as outfile:
    outfile.write(dtemp.render({'rows':rows}))
