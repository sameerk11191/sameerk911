import pandas as pd
import re
from sqlalchemy import create_engine



mv = pd.read_excel('data/mv_dirty.xls',
                       skiprows=5,
                       header=0,
                       skipfooter=14,
                       na_values='(NA)',
                       index_col=[0,1,2,3])


mv.dropna(how='all', inplace=True)
mv= mv.reset_index()
new = mv["Mobility period"].str.split(" ", n = 1, expand=True)
mv["Mobility period (year)"] = new[0]
mv["Mobility period (details)"] = new[1]
mv.drop(columns=["Mobility period"], inplace=True)

mv.rename(columns={mv.columns[3] : 'Diff_residence:total',
                       mv.columns[4] : 'Diff_residence_Same_country',
                       mv.columns[5] : 'Diff_country_total',
                       mv.columns[6] : 'Diff_country_Same_state',
                       mv.columns[7] : 'Diff_country_Diff_state',
                       mv.columns[8] : 'Movers_from_abroad' }
              , inplace=True)



mv = mv.iloc[1:]

cols = mv.columns.tolist()
cols = cols[-1:] + cols[:-1]
cols = cols[-1:] + cols[:-1]
mv = mv[cols]


mv.to_excel(excel_writer='data/mv_clean123.xls',
                sheet_name='mv',
                na_rep='null',
                index=False)

sqlite = create_engine('sqlite:///data/sk2.db')

mv.to_sql('mv',
              sqlite,
              if_exists='replace',
              index=False)

sqlite.dispose()
