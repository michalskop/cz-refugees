"""Prepare origin file."""

import pandas as pd
import numpy as np

path = "/home/michal/dev/sz/war/cz-refugees/"

pretty = pd.read_csv(path + "origin/pretty_municipalities.csv")
orig = pd.read_csv(path + "origin/origin.csv")

orig_merged = orig.merge(pretty.loc[:, ['district', 'pretty_name', 'name', 'code']], how="left", on="code")
orig_merged.columns

orig_merged.to_csv(path + "origin.csv", index=False)

fname = 'Strpeni-UKR_-_k_11-03-2022.xlsx'
data = pd.read_excel(path + 'data/' + fname)
values = data.columns[5:]
pd.pivot_table(data, values=values, index=['obec', 'okres'], aggfunc=np.sum)

orig_merged.merge(data, how="left", left_on=['district', 'name'], right_on=['okres', 'obec']).fillna(0)