import streamlit as st
import pandas as pd
import numpy as np

def highlight_row(row):
    return ['font-weight: bold' if row.name == len(df) - 1 else '' for _ in row]

st.set_page_config(
        page_title="Pending FoCs in Finance - report generator",
)

def all_pending(file):
  import pandas as pd
  import numpy as np

  pend = pd.read_excel(file, engine = "openpyxl")
  pend.columns = pend.iloc[1]
  pend = pend[2:]
  pend['DEPARTMENT NAME2'] = np.where(pend['DEPARTMENT NAME'].isin(['Public Works (Buildings & NH) Department', 'Public Works (Roads) Department']), 'PWD', 'Non PWD')
  SOPD_list = ['SOPD-FDR', 'SOPD-G', 'SOPD-GSP', 'SOPD-ODS', 'SOPD-SCSP', 'SOPD-TSP']
  RIDF_list = ['RIDF-LS', 'RIDF-SS', 'WIF-LS', 'WIF-SS', 'UIDF-LS', 'UIDF-SS']
  TG_list = ['TG-AC', 'TG-DC', 'TG-EI', 'TG-FFC', 'TG-IB', 'TG-SFC', 'TG-SSA', 'TG-UL']
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
                                                                                                                        pend['SCHEME CODE']))))))))
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
  dfx1 = pend[(pend['SCHEME NAME2']!='CSS') & (pend['SCHEME NAME2']!='SOPD') & (pend['Rev-Cap']=='Capital')].groupby(['SCHEME NAME2'])['REQUESTED AMOUNT'].sum().round(2).reset_index()
  dfx1.columns = ['SCHEME NAME2', 'Capital']
  df1 = df1.merge(dfx1, on='SCHEME NAME2', how='left')

  df2 = pend[(pend['SCHEME NAME2']!='CSS') & (pend['SCHEME NAME2']=='SOPD')].groupby(['SCHEME NAME2', 'DEPARTMENT NAME2'])['REQUESTED AMOUNT'].sum().round(2).reset_index()
  dfx2 = pend[(pend['SCHEME NAME2']!='CSS') & (pend['SCHEME NAME2']=='SOPD') & (pend['Rev-Cap']=='Capital')].groupby(['SCHEME NAME2', 'DEPARTMENT NAME2'])['REQUESTED AMOUNT'].sum().round(2).reset_index()
  dfx2.columns = ['SCHEME NAME2', 'DEPARTMENT NAME2', 'Capital']
  df2 = df2.merge(dfx2, on=['SCHEME NAME2', 'DEPARTMENT NAME2'], how='left')
  
  df3 = pd.concat([df1, df2], ignore_index=True).sort_values('SCHEME NAME2')
  df3.index = np.arange(len(df3))
  df3.loc[len(df3)] = ['Total', '', df3['REQUESTED AMOUNT'].sum().round(2), pend[(pend['SCHEME NAME2']!='CSS') & (pend['Rev-Cap']=='Capital')]['REQUESTED AMOUNT'].sum().round(2)]
  
  df3.columns = ['Scheme', 'Dept', 'Requested amount (Cr.)', 'Capital (Cr.)']
  df3.fillna('', inplace=True)
  df3 = df3.style.apply(highlight_row, axis=1)

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
  TG_list = ['TG-AC', 'TG-DC', 'TG-EI', 'TG-FFC', 'TG-IB', 'TG-SFC', 'TG-SSA', 'TG-UL']
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
                                                                                                                        pend['SCHEME CODE']))))))))
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
  dfx1 = pend[(pend['SCHEME NAME2']!='CSS') & (pend['Hierarchy']=='Seniormost') & (pend['SCHEME NAME2']!='SOPD') & (pend['Rev-Cap']=='Capital')].groupby(['SCHEME NAME2'])['REQUESTED AMOUNT'].sum().round(2).reset_index()
  dfx1.columns = ['SCHEME NAME2', 'Capital']
  df1 = df1.merge(dfx1, on='SCHEME NAME2', how='left')

  df2 = pend[(pend['SCHEME NAME2']!='CSS') & (pend['Hierarchy']=='Seniormost') & (pend['SCHEME NAME2']=='SOPD')].groupby(['SCHEME NAME2', 'DEPARTMENT NAME2'])['REQUESTED AMOUNT'].sum().round(2).reset_index()
  dfx2 = pend[(pend['SCHEME NAME2']!='CSS') & (pend['Hierarchy']=='Seniormost') & (pend['SCHEME NAME2']=='SOPD') & (pend['Rev-Cap']=='Capital')].groupby(['SCHEME NAME2', 'DEPARTMENT NAME2'])['REQUESTED AMOUNT'].sum().round(2).reset_index()
  dfx2.columns = ['SCHEME NAME2', 'DEPARTMENT NAME2', 'Capital']
  df2 = df2.merge(dfx2, on=['SCHEME NAME2', 'DEPARTMENT NAME2'], how='left')

  df3 = pd.concat([df1, df2], ignore_index=True).sort_values('SCHEME NAME2')
  df3.index = np.arange(len(df3))
  df3.loc[len(df3)] = ['Total', '', df3['REQUESTED AMOUNT'].sum().round(2), pend[(pend['SCHEME NAME2']!='CSS') & (pend['Hierarchy']=='Seniormost') & (pend['Rev-Cap']=='Capital')]['REQUESTED AMOUNT'].sum().round(2)]
  
  df3.columns = ['Scheme', 'Dept', 'Requested amount (Cr.)', 'Capital (Cr.)']
  df3.fillna('', inplace=True)
  df3 = df3.style.apply(highlight_row, axis=1)
        
  return df3


st.title("Pending FoCs in Finance - report generator")

uploaded_file = st.file_uploader("Upload file"
                                 , type = ['xlsx']
                                )

st.header("Senior Most")
try:
  st.dataframe(seniormost(uploaded_file))
except ValueError:
  st.write("*Upload file to generate report* :scroll:")

st.header("All (including Senior Most)")
try:
  st.dataframe(all_pending(uploaded_file))
except ValueError:
  st.write("*Upload file to generate report* :scroll:")
