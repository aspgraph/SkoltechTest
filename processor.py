import pandas as pd


def process_incidents(*, input_filename, output_filename, dT):
    if dT < 0.0 or dT > 1.0:
        print('Wrong arguments! Requirements: M >= 1, 0.0 <= dT <= 1.0')
        return

    try:
        df = pd.read_csv(input_filename, header=0)
    except IOError:
        print('Could not read file:', input_filename)
        return

    res = []
    skip_count = 0
    df.sort_values(by='time', inplace=True)
    grp = df.groupby(by=['feature1', 'feature2'], sort=False)
    for grp_index, grp_rows in grp:
        cur_i = 0
        last_i = 0
        prev_time = -1.0
        last_index = grp_rows.index[last_i]
        for cur_index in grp_rows.index:
            cur_time = grp_rows.at[cur_index, 'time']
            last_time = grp_rows.at[last_index, 'time']
            if prev_time == cur_time:
                skip_count += 1
            while cur_time >= last_time + dT:
                last_i += 1
                last_index = grp_rows.index[last_i]
                new_time = grp_rows.at[last_index, 'time']
                if last_time == new_time:
                    skip_count -= 1
                last_time = new_time
            res.append((cur_index, cur_i - last_i - skip_count))
            prev_time = cur_time
            cur_i += 1
    res.sort()
    ndf = pd.DataFrame.from_records(res, columns=['id', 'count'])

    try:
        ndf.to_csv(output_filename, index=False)
    except IOError:
        print('Could not write file:', output_filename)
        return
