"""Prepare first data for a map."""

import datetime
import pandas as pd
import numpy as np

origin = pd.read_csv('origin.csv')

# today = datetime.datetime.today()
# todate = today.strftime('%d-%m-%Y')

fname = 'Strpeni-UKR_-_k_10-03-2022.xlsx'
fname = 'Strpění_UKR_13_3_2022.xlsx'
fname = 'Statistika_UKR_17_04_2022.xlsx'

today = (datetime.datetime.today())
todate = today.strftime("%-d. %-m. %Y")

# municipalities
data = pd.read_excel('data/' + fname)
values = data.columns[5:]	# added municipality codes
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
out['celkem'] = out['celkem'].astype(int)
out['date'] = todate

out.to_csv('municipalities.csv', index=False)

# regions
origino = pd.read_csv('origin_okresy.csv')

out['population'] = out['počet obyv.'].str.replace(' ', '').astype(int)

pto = pd.pivot_table(out, values=(list(values) + ages + ['population']), index='district' , aggfunc=np.sum).reset_index()

pto['celkem'] = pto['celkem'].astype(int)
pto['population'] = pto['population'].astype(int)

outo = origino.merge(pto, how="left", left_on='name', right_on='district').fillna(0)

outo['rate'] = (outo['celkem'] / outo['population'] * 100).round(2)

outo['date'] = todate

outo.to_csv('districts.csv', index=False, columns=(list(origino.columns) + ['population', 'rate'] + list(values) + ages + ['date']))
