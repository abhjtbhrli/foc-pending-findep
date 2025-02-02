import streamlit as st
import pandas as pd
import numpy as np

def all_pending(file):
  import pandas as pd
  import numpy as np

  pend = pd.read_excel(file, engine = "openpyxl")
  pend.columns = pend.iloc[1]
  pend = pend[2:]
  pend['DEPARTMENT NAME2'] = np.where(pend['DEPARTMENT NAME'].isin(['Public Works (Buildings & NH) Department', 'Public Works (Roads) Department']), 'PWD', 'Non PWD')
  SOPD_list = ['SOPD-FDR', 'SOPD-G', 'SOPD-GSP', 'SOPD-ODS', 'SOPD-SCSP', 'SOPD-TSP']
  RIDF_list = ['RIDF-LS', 'RIDF-SS', 'WIF-LS', 'WIF-SS', 'UIDF-LS', 'UIDF-SS']
  TG_list = ['TG-IB', 'TG-SFC', 'TG-UL']
  EE_list = ['EE-CS', 'EE-SS']
  pend['SCHEME NAME2'] = np.where(pend['SCHEME CODE'].isin(['CSS', 'SOPD-SS']),
                                'CSS',
                                np.where(pend['SCHEME CODE'].isin(['EAP', 'EAP-SS']),
                                         'EAP',
                                         np.where(pend['SCHEME CODE'].isin(['NIDA-LS', 'NIDA-SS']),
                                                  'NIDA',
                                                  np.where(pend['SCHEME CODE'].isin(RIDF_list),
                                                                                    'RIDF',
                                                                                    np.where(pend['SCHEME CODE'].isin(SOPD_list),
                                                                                             'SOPD',
                                                                                             np.where(pend['SCHEME CODE'].isin(TG_list),
                                                                                                      'TG',
                                                                                                      np.where(pend['SCHEME CODE']=='EE',
                                                                                                               'EE',
                                                                                                               np.where(pend['SCHEME CODE'].isin(EE_list),
                                                                                                                        'EE (CS + SS)',
                                                                                                                        'Others'))))))))
  pend['MH'] = pend['HEAD OF ACCOUNT'].str.slice(0,4)
  pend['MH'] = pd.to_numeric(pend['MH'])
  pend['Rev-Cap'] = np.where((pend['MH']<3999) & (pend['MH']>=2000),
                           'Revenue',
                           np.where((pend['MH']<5999) & (pend['MH']>=4000),
                                    'Capital',
                                    'Loans & Advances'))
  SENIORMOST_list = ['Mr.Dilip Kumar BorahIAS,Secretary', 'Mr.JayantNarlikar , IAS ,Commissioner & Secretary', 'Mr.Hemanta Kumar Dewri,Special Secretary']
  pend['Hierarchy'] = np.where(pend['HELD BY'].isin(SENIORMOST_list), 'Seniormost', 'Non Seniormost')
  pend['REQUESTED AMOUNT'] = pend['REQUESTED AMOUNT'].apply(lambda x:x/100)

  df1 = pend[(pend['SCHEME NAME2']!='CSS') & (pend['SCHEME NAME2']!='SOPD')].groupby(['SCHEME NAME2'])['REQUESTED AMOUNT'].sum().round(2).reset_index()
  df1['DEPARTMENT NAME2'] = ''
  df1 = df1[['SCHEME NAME2', 'DEPARTMENT NAME2', 'REQUESTED AMOUNT']]

  df2 = pend[(pend['SCHEME NAME2']!='CSS') & (pend['SCHEME NAME2']=='SOPD')].groupby(['SCHEME NAME2', 'DEPARTMENT NAME2'])['REQUESTED AMOUNT'].sum().round(2).reset_index()

  df3 = pd.concat([df1, df2], ignore_index=True).sort_values('SCHEME NAME2')
  df3.index = np.arange(len(df3))
  df3.loc[len(df3)] = ['Total', '', df3['REQUESTED AMOUNT'].sum().round(2)]
  df3.loc[len(df3)] = ['Capital', '', pend[(pend['SCHEME NAME2']!='CSS') & (pend['Rev-Cap']=='Capital')]['REQUESTED AMOUNT'].sum().round(2)]
  df3.columns = ['Scheme', 'Dept', 'Requested amount (Cr.)']

  return df3

def seniormost(file):
  import pandas as pd
  import numpy as np

  pend = pd.read_excel(file, engine = "openpyxl")
  pend.columns = pend.iloc[1]
  pend = pend[2:]
  pend['DEPARTMENT NAME2'] = np.where(pend['DEPARTMENT NAME'].isin(['Public Works (Buildings & NH) Department', 'Public Works (Roads) Department']), 'PWD', 'Non PWD')
  SOPD_list = ['SOPD-FDR', 'SOPD-G', 'SOPD-GSP', 'SOPD-ODS', 'SOPD-SCSP', 'SOPD-TSP']
  RIDF_list = ['RIDF-LS', 'RIDF-SS', 'WIF-LS', 'WIF-SS', 'UIDF-LS', 'UIDF-SS']
  TG_list = ['TG-IB', 'TG-SFC', 'TG-UL']
  EE_list = ['EE-CS', 'EE-SS']
  pend['SCHEME NAME2'] = np.where(pend['SCHEME CODE'].isin(['CSS', 'SOPD-SS']),
                                'CSS',
                                np.where(pend['SCHEME CODE'].isin(['EAP', 'EAP-SS']),
                                         'EAP',
                                         np.where(pend['SCHEME CODE'].isin(['NIDA-LS', 'NIDA-SS']),
                                                  'NIDA',
                                                  np.where(pend['SCHEME CODE'].isin(RIDF_list),
                                                                                    'RIDF',
                                                                                    np.where(pend['SCHEME CODE'].isin(SOPD_list),
                                                                                             'SOPD',
                                                                                             np.where(pend['SCHEME CODE'].isin(TG_list),
                                                                                                      'TG',
                                                                                                      np.where(pend['SCHEME CODE']=='EE',
                                                                                                               'EE',
                                                                                                               np.where(pend['SCHEME CODE'].isin(EE_list),
                                                                                                                        'EE (CS + SS)',
                                                                                                                        'Others'))))))))
  pend['MH'] = pend['HEAD OF ACCOUNT'].str.slice(0,4)
  pend['MH'] = pd.to_numeric(pend['MH'])
  pend['Rev-Cap'] = np.where((pend['MH']<3999) & (pend['MH']>=2000),
                           'Revenue',
                           np.where((pend['MH']<5999) & (pend['MH']>=4000),
                                    'Capital',
                                    'Loans & Advances'))
  SENIORMOST_list = ['Mr.Dilip Kumar BorahIAS,Secretary', 'Mr.JayantNarlikar , IAS ,Commissioner & Secretary', 'Mr.Hemanta Kumar Dewri,Special Secretary']
  pend['Hierarchy'] = np.where(pend['HELD BY'].isin(SENIORMOST_list), 'Seniormost', 'Non Seniormost')
  pend['REQUESTED AMOUNT'] = pend['REQUESTED AMOUNT'].apply(lambda x:x/100)

  df1 = pend[(pend['SCHEME NAME2']!='CSS') & (pend['Hierarchy']=='Seniormost') & (pend['SCHEME NAME2']!='SOPD')].groupby(['SCHEME NAME2'])['REQUESTED AMOUNT'].sum().round(2).reset_index()
  df1['DEPARTMENT NAME2'] = ''
  df1 = df1[['SCHEME NAME2', 'DEPARTMENT NAME2', 'REQUESTED AMOUNT']]

  df2 = pend[(pend['SCHEME NAME2']!='CSS') & (pend['Hierarchy']=='Seniormost') & (pend['SCHEME NAME2']=='SOPD')].groupby(['SCHEME NAME2', 'DEPARTMENT NAME2'])['REQUESTED AMOUNT'].sum().round(2).reset_index()

  df3 = pd.concat([df1, df2], ignore_index=True).sort_values('SCHEME NAME2')
  df3.index = np.arange(len(df3))
  df3.loc[len(df3)] = ['Total', '', df3['REQUESTED AMOUNT'].sum().round(2)]
  df3.loc[len(df3)] = ['Capital', '', pend[(pend['SCHEME NAME2']!='CSS') & (pend['Hierarchy']=='Seniormost') & (pend['Rev-Cap']=='Capital')]['REQUESTED AMOUNT'].sum().round(2)]
  df3.columns = ['Scheme', 'Dept', 'Requested amount (Cr.)']

  return df3

st.title("Pending FoCs in Finance - report generator")

uploaded_file = st.file_uploader("Upload file"
                                 , type = ['xlsx']
                                )

st.heading("Senior Most")
try:
  st.dataframe(seniormost(uploaded_file))
except ValueError:
  st.write("*Upload file to generate report* :scroll:")

st.heading("All (including Senior Most)")
try:
  st.dataframe(all_pending(uploaded_file))
except ValueError:
  st.write("*Upload file to generate report* :scroll:")
