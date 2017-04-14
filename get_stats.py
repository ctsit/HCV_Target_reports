import json

with open('time_trimmed.json', 'r') as infile:
    data = infile.read()

subject_stats = {}
for key in data.keys():
    subject_stats[key] = {}

def get_mean(records, baseline, field):
    sum = 0.0
    record_num = 0
    records += baseline
    for record in records:
        try:
            sum += float( record[field] )
            record_num += 1
        except:
            pass
    return sum/record_num

def get_std_dev(records, baseline, field):
    mean = get_mean(records, baseline field)
    record_num = 0
    sum = 0.0
    records += baseline
    for record in records:
        try:
            sum += (float(record[field]) - mean)**2
            record_num += 1
        except:
            pass
    return (sum / record_num) ** 0.5

def get_delta(records, baseline, field, date_field):
    records += baseline
    curr_max = baseline[date_field]
    for record in records:
        pass
    return None

