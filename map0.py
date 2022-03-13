"""Prepare first data for a map."""

import datetime
import pandas as pd
import numpy as np

origin = pd.read_csv('origin.csv')

# today = datetime.datetime.today()
# todate = today.strftime('%d-%m-%Y')

fname = 'Strpeni-UKR_-_k_10-03-2022.xlsx'
fname = 'Strpění_UKR_12_3_2022.xlsx'
data = pd.read_excel('data/' + fname)
values = data.columns[4:]
pt = pd.pivot_table(data, values=values, index=['obec', 'okres'], aggfunc=np.sum)

out = origin.merge(pt, how="left", left_on=['district', 'name'], right_on=['okres', 'obec']).fillna(0)

genders = ['z', 'm', 'x']
ages = ['do_3', 'do_6', 'do_15', 'do_18', 'do_65', 'sen']

for age in ages:
	selected = []
	for g in genders:
		if g + "_" + age in values:
			selected.append(g + "_" + age)
	out[age] = out.loc[:, selected].sum(axis=1)

out['rate'] = (out['celkem'] / out['počet obyv.'].str.replace(' ', '').astype(int) * 100).round(2)

del out['pretty_name']

out.to_csv('municipalities.csv', index=False)