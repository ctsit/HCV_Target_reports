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

def date_diff(date1, date2):
    print(date1, date2)
    if not ( date1 and date2 ):
        return 0
    ymd1 = [int(item) for item in date1.split('-')]
    ymd2 = [int(item) for item in date2.split('-')]

    diffs = [ymd1[i] - ymd2[i] for i in range(0, 3)]

    week_diff = [diffs[0] * 52, diffs[1] * 4, diffs[2] / 7.0]
    diff = abs(sum(week_diff))
    return diff


def get_follow_up_stats(recs, form_str):
    # baseline is first rec
    date_key = "{}_im_lbdtc".format(form_str)
    ttff = "{}_weeks_to_first_followup".format(form_str)
    ttlf = "{}_week_to_last_followup".format(form_str)
    fuperiod = "{}_followup_period_weeks_length".format(form_str)
    base_date = recs[0].get(date_key)
    first_fu_date = base_date
    last_fu_date = base_date
    # first follow up will be the second record
    if len(recs) > 1:
        first_fu_date = recs[1].get(date_key)
    # get time to first fu
    # get last record, get time to last fu
    if len(recs) > 1:
        last_fu_date = recs[-1].get(date_key)
    # get range over which it happened
    return {
        ttff: date_diff(base_date, first_fu_date),
        ttlf: date_diff(base_date, last_fu_date),
        fuperiod: date_diff(first_fu_date, last_fu_date)
    }

