"""Prepare data for a map."""

import datetime
import pandas as pd
import numpy as np

origin = pd.read_csv('origin.csv')


fname = 'Strpeni-UKR_-_k_11-03-2022.xlsx'
data = pd.read_excel('data/' + fname)
values = data.columns[5:]
pd.pivot_table(data, values=values, index=['obec', 'okres'], aggfunc=np.sum)

orig_merged.merge(data, how="left", left_on=['district', 'name'], right_on=['okres', 'obec']).fillna(0)