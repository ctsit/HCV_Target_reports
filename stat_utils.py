def get_mean(records, field):
    sum = 0.0
    record_num = 0
    for record in records:
        try:
            sum += float( record[field] )
            record_num += 1
        except:
            pass
    return sum/record_num if record_num else 'No mean'

def get_std_dev(records, field):
    mean = get_mean(records, field)
    record_num = 0
    sum = 0.0
    for record in records:
        try:
            sum += (float(record[field]) - mean)**2
            record_num += 1
        except:
            pass
    return (sum / record_num) ** 0.5 if record_num else 'No standard deviation'

def get_delta(records, field, date_field):
    records = sorted(records, key=lambda r: r[date_field])
    step_delta = [float(records[index - 1][field]) - float(r[field]) for index, r in enumerate(records) if index != 0]
    total_delta = 0
    for delta in step_delta:
        total_delta += delta
    return ( total_delta, step_delta ) if len(records) else ( 'No records to get delta', 'No records to get deltas' )

def get_max(records, field):
    recs = [float( rec.get(field) ) for rec in records if rec.get(field)]
    return max(recs) if len(recs) else 'No records with value'

def get_min(records, field):
    recs = [float( rec.get(field) ) for rec in records if rec.get(field)]
    return min(recs) if len(recs) else 'No records with value'
