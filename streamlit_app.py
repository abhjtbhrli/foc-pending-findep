import streamlit as st
import pandas as pd
import numpy as np
from google.oauth2.service_account import Credentials
import gspread

st.set_page_config(
        page_title="CDM Ceiling reports",
)

SHEET_ID = "1yrNlRXU8Zub6_4DD8L_a1xi3sBHV1UsG0w3dkVSAvr8"
GID = "862709843"   # your tab gid (string)

creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=["https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"]
)
gc = gspread.authorize(creds)
sh = gc.open_by_key(SHEET_ID)

# get worksheet by gid
ws = next(ws for ws in sh.worksheets() if str(ws.id) == GID)

def all_pending(file):
  import pandas as pd
  import numpy as np

  pend = pd.read_excel(file, engine = "openpyxl")
  pend.columns = pend.iloc[0].tolist()
  pend = pend[2:]
  pend['DEPARTMENT NAME2'] = np.where(pend['DEPARTMENT NAME'].isin(['Public Works (Buildings & NH) Department', 'Public Works (Roads) Department', 'Public Works (Health and Education) Department']), 'PWD', 'Non PWD')
  SOPD_list = ['SOPD-FDR', 'SOPD-G', 'SOPD-GSP', 'SOPD-ODS', 'SOPD-SCSP', 'SOPD-TSP']
  RIDF_list = ['RIDF-LS', 'RIDF-SS', 'WIF-LS', 'WIF-SS', 'UIDF-LS', 'UIDF-SS', 'SCDF-LS', 'SCDF-SS']
  TG_list = ['TG-AC', 'TG-DC', 'TG-EI', 'TG-FFC', 'TG-IB', 'TG-SFC', 'TG-SSA', 'TG-UL', 'TG-CFC']
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

  return df3

def seniormost(file):
  import pandas as pd
  import numpy as np

  pend = pd.read_excel(file, engine = "openpyxl")
  pend.columns = pend.iloc[0].tolist()
  pend = pend[2:]
  pend['DEPARTMENT NAME2'] = np.where(pend['DEPARTMENT NAME'].isin(['Public Works (Buildings & NH) Department', 'Public Works (Roads) Department', 'Public Works (Health and Education) Department']), 'PWD', 'Non PWD')
  SOPD_list = ['SOPD-FDR', 'SOPD-G', 'SOPD-GSP', 'SOPD-ODS', 'SOPD-SCSP', 'SOPD-TSP']
  RIDF_list = ['RIDF-LS', 'RIDF-SS', 'WIF-LS', 'WIF-SS', 'UIDF-LS', 'UIDF-SS', 'SCDF-LS', 'SCDF-SS']
  TG_list = ['TG-AC', 'TG-DC', 'TG-EI', 'TG-FFC', 'TG-IB', 'TG-SFC', 'TG-SSA', 'TG-UL', 'TG-CFC']
  EE_list = ['EE-CS', 'EE-SS']

  pend['MH'] = pend['HEAD OF ACCOUNT'].str.slice(0,4)
  pend['MH'] = pd.to_numeric(pend['MH'])
  pend['Rev-Cap'] = np.where((pend['MH']<3999) & (pend['MH']>=2000),
                           'Revenue',
                           np.where((pend['MH']<5999) & (pend['MH']>=4000),
                                    'Capital',
                                    'Loans & Advances'))
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
        
  return df3

def css_ss(file):
  import pandas as pd
  import numpy as np
  css_df = pd.read_excel(file, engine = "openpyxl")
  css_df.columns = css_df.iloc[0].tolist()
  css_df = css_df[2:]
  css_df = css_df[css_df['SCHEME CODE'].isin(['CSS', 'TG-CFC'])]
  css_df['MH'] = css_df['HEAD OF ACCOUNT'].str.slice(0,4)
  css_df['MH'] = pd.to_numeric(css_df['MH'])
  css_df['Rev-Cap'] = np.where((css_df['MH']<3999) & (css_df['MH']>=2000),
                           'Revenue',
                           np.where((css_df['MH']<5999) & (css_df['MH']>=4000),
                                    'Capital',
                                    'Loans & Advances'))
  css_df = css_df[['SCHEME CODE', 'Rev-Cap', 'DEPARTMENT NAME', 'SCHEME NAME', 'REQUESTED AMOUNT', 'HEAD OF ACCOUNT', 'PROPOSAL DATE']]
  css_df['REQUESTED AMOUNT'] = css_df['REQUESTED AMOUNT'].apply(lambda x:x/100).round(2)
  css_df = css_df.sort_values(by=['Rev-Cap', 'PROPOSAL DATE'], ascending=True).reset_index()
  css_df = css_df[['SCHEME CODE', 'Rev-Cap', 'DEPARTMENT NAME', 'SCHEME NAME', 'REQUESTED AMOUNT', 'HEAD OF ACCOUNT', 'PROPOSAL DATE']]
  css_df.loc[len(css_df)] = ['', '', '', '', css_df['REQUESTED AMOUNT'].sum().round(2), '', ''] 
  return css_df


def sopd_ss(file):
  import pandas as pd
  import numpy as np
  sopd_ss_df = pd.read_excel(file, engine = "openpyxl")
  sopd_ss_df.columns = sopd_ss_df.iloc[0].tolist()
  sopd_ss_df = sopd_ss_df[2:]
  sopd_ss_df = sopd_ss_df[sopd_ss_df['SCHEME CODE'].isin(['SOPD-SS'])]
  sopd_ss_df['MH'] = sopd_ss_df['HEAD OF ACCOUNT'].str.slice(0,4)
  sopd_ss_df['MH'] = pd.to_numeric(sopd_ss_df['MH'])
  sopd_ss_df['Rev-Cap'] = np.where((sopd_ss_df['MH']<3999) & (sopd_ss_df['MH']>=2000),
                           'Revenue',
                           np.where((sopd_ss_df['MH']<5999) & (sopd_ss_df['MH']>=4000),
                                    'Capital',
                                    'Loans & Advances'))
  sopd_ss_df = sopd_ss_df[['SCHEME CODE', 'Rev-Cap', 'DEPARTMENT NAME', 'SCHEME NAME', 'REQUESTED AMOUNT', 'HEAD OF ACCOUNT', 'PROPOSAL DATE']]
  sopd_ss_df['REQUESTED AMOUNT'] = sopd_ss_df['REQUESTED AMOUNT'].apply(lambda x:x/100).round(2)
  sopd_ss_df = sopd_ss_df.sort_values(by=['Rev-Cap', 'PROPOSAL DATE'], ascending=True).reset_index()
  sopd_ss_df = sopd_ss_df[['SCHEME CODE', 'Rev-Cap', 'DEPARTMENT NAME', 'SCHEME NAME', 'REQUESTED AMOUNT', 'HEAD OF ACCOUNT', 'PROPOSAL DATE']]
  sopd_ss_df.loc[len(sopd_ss_df)] = ['', '', '', '', sopd_ss_df['REQUESTED AMOUNT'].sum().round(2), '', '']
  return sopd_ss_df

def pipeline(file1, file2):
  import pandas as pd
  import numpy as np
  pipe = pd.read_excel(file1, engine = "openpyxl")
  pipe.columns = pipe.iloc[0].tolist()
  pipe = pipe[2:]
  pipe['DH'] = pipe['HEAD OF ACCOUNT'].str[-5:]
  pipe['MH'] = pipe['HEAD OF ACCOUNT'].str[:1]
  pipe['ISSUED ON'] = pd.to_datetime(pipe['ISSUED ON'])
  today = pd.to_datetime("today").normalize()
  pipe["Days"] = (today - pipe["ISSUED ON"]).dt.days
  excl = ['FIN/DIS/TAX/001/2025/1471',
'FIN/DIS/POL/001/2025/16629',
'FIN/KAM/POL/001/2025/16634',
'FIN/KAM/POL/001/2025/16633',
'FIN/KAM/POL/001/2025/16632',
'FIN/KAM/POL/001/2025/16631',
'FIN/KAM/POL/001/2025/16630',
'FIN/NLB/PWB/001/2025/13102',
'FIN/DIS/EE/025/2025/1715',
'FIN/DIS/EE/025/2025/1718',
'FIN/DIS/HS/017/2025/2066',
'FIN/DIS/HS/017/2025/2068',
'FIN/NGT/SCD/001/2025/1575',
'FIN/NGT/SWD/001/2025/4960',
'FIN/DIS/HS/017/2025/2075',
'FIN/DIS/HS/017/2025/2082',
'FIN/DIS/SAD/001/2025/4526',
'FIN/DIS/MDB/002/2025/1361',
'FIN/DIS/SCE/001/2025/1168',
'FIN/DIS/SCE/001/2025/1169',
'FIN/DIS/DMA/001/2025/047',
'FIN/DIS/DMA/001/2025/046',
'FIN/DIS/SAD/001/2025/4605',
'FIN/DIS/SAD/001/2025/4614',
'FIN/DIS/MDA/001/2025/1536',
'FIN/DIS/SAD/001/2025/4572',
'FIN/DIS/AGR/001/2025/1860',
'FIN/DIS/EE/025/2025/1730',
'FIN/DIS/HT/001/2025/1396',
'FIN/DIS/ST/001/2025/614',
'FIN/HFL/HAC/001/2025/1238',
'FIN/DPU/KAC/001/2025/3059',
'FIN/HFL/HAC/001/2025/1237',
'FIN/DPU/KAC/001/2025/3058',
'FIN/DIS/TCP/001/2025/1367',
'FIN/DIS/EE/025/2025/1736',
'FIN/KAM/IWT/001/2025/1722',
'FIN/DIS/AGR/001/2025/1859',
'FIN/DIS/TRA/001/2025/1216', 'FIN/DIS/DME/001/2025/2890', 'FIN/DIS/AGR/001/2025/1861', 'FIN/DIS/AGR/001/2025/1881', 'FIN/DIS/AGR/001/2025/1882', 'FIN/DIS/SCE/001/2025/1196', 'FIN/DIS/SCE/001/2025/1195', 'FIN/DIS/SCE/001/2025/1198', 'FIN/DIS/SCE/001/2025/1197', 'FIN/DIS/MDA/001/2025/1630',
'FIN/DIS/TCP/005/2025/1399',
'FIN/DIS/SAD/001/2025/4771',
'FIN/DIS/AGR/001/2025/1932',
'FIN/DIS/AGR/001/2025/1934',
'FIN/DIS/EE/025/2025/1867',
'FIN/DIS/EE/001/2025/1866',
'FIN/DIS/PRD/001/2025/1673',
'FIN/DIS/SCE/001/2025/1209',
'FIN/DIS/SWD/011/2025/4371',
'FIN/DIS/ST/001/2025/623']

  pipe['Excl'] = pipe['CEILING NO'].apply(lambda x:"Yes" if x in excl else "No")

  foc = pd.read_csv(file2)
  sheet_id = "1yrNlRXU8Zub6_4DD8L_a1xi3sBHV1UsG0w3dkVSAvr8"
  gid = "862709843"  # the tab gid from your URL
  csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
  focno = pd.read_csv(csv_url)
  exp_list = list(set(focno['Foc Number'].unique().tolist()+foc['Foc Number'].unique().tolist()))
  pipe['Exp'] = pipe['CEILING NO'].apply(lambda x:"Yes" if x in exp_list else "No")
  
  rows_to_append = [[str(x)] for x in foc['Foc Number'].dropna().astype(str)]
  header = ws.row_values(1)
  col_idx = header.index("Foc Number") + 1
  start_row = len(ws.get_all_values()) + 1
  # write down the column (A1 range)
  ws.update(
      gspread.utils.rowcol_to_a1(start_row, col_idx),
      rows_to_append
  )

  SOPD_list = ['SOPD-FDR', 'SOPD-G', 'SOPD-GSP', 'SOPD-ODS', 'SOPD-SCSP', 'SOPD-TSP']
  RIDF_list = ['RIDF-LS', 'RIDF-SS', 'WIF-LS', 'WIF-SS', 'UIDF-LS', 'UIDF-SS', 'SCDF-LS', 'SCDF-SS']
  TG_list = ['TG-AC', 'TG-DC', 'TG-EI', 'TG-FFC', 'TG-IB', 'TG-SFC', 'TG-SSA', 'TG-UL', 'TG-CFC']
  CSS_list = ['CSS', 'SOPD-SS', 'EE-CS', 'EE-SS']
  EAP_list = ['EAP', 'EAP-SS']
  NIDA_list = ['NIDA-LS', 'NIDA-SS']
  pipe['SCHEME CODE2'] = np.where(pipe['SCHEME CODE'].isin(SOPD_list),
                                   'SOPD',
                                   np.where(pipe['SCHEME CODE'].isin(RIDF_list),
                                            'RIDF',
                                            np.where(pipe['SCHEME CODE'].isin(TG_list),
                                                     'TG',
                                                     np.where(pipe['SCHEME CODE'].isin(CSS_list),
                                                              'CSS',
                                                              np.where(pipe['SCHEME CODE'].isin(EAP_list),
                                                                       'EAP',
                                                                       np.where(pipe['SCHEME CODE'].isin(NIDA_list),
                                                                                'NIDA',
                                                                                pipe['SCHEME CODE']))))))
  pipe['Rev-Cap'] = np.where(pipe['MH'].isin(['2','3']),
                             'Revenue',
                             np.where(pipe['MH'].isin(['4','5']),
                                      'Capital',
                                      'Loans & Advances'))
  pipe['APPROVED AMOUNT'] = pipe['APPROVED AMOUNT'].apply(lambda x:x/100)
  pipex = pipe[['SCHEME CODE2', 'Rev-Cap', 'APPROVED AMOUNT','Days','Excl','Exp','DH']]
  pipex = pipex[pipex['Days']<=15]
  pipex = pipex[pipex['Exp']=='No']
  pipex = pipex[pipex['Excl']=='No']
  csv = pipe[(pipe['Days']<=15) & (pipe['Exp']=='No') & (pipe['Excl']=='No')].to_csv(index=False).encode("utf-8")
  pipex_rep = pipex.groupby(['SCHEME CODE2'])['APPROVED AMOUNT'].sum().round(2).reset_index()
  pipex_rep_cap = pipex[pipex['Rev-Cap']=='Capital'].groupby(['SCHEME CODE2'])['APPROVED AMOUNT'].sum().round(2).reset_index()
  pipex_rep = pipex_rep.merge(pipex_rep_cap, how='left', on='SCHEME CODE2')
  pipex_rep.fillna(0, inplace = True)
  pipex_rep.columns = ['Scheme', 'Approved amount (Cr.)', 'Capital (Cr.)']

  pipex_rep.loc[len(pipex_rep)] = ['Total', pipex_rep['Approved amount (Cr.)'].sum().round(2), pipex_rep['Capital (Cr.)'].sum().round(2)]

  return pipex_rep, csv

st.markdown("""
<h1 style='text-align: center;'>Ceiling Reports</h1>
<p style='text-align: center; font-style: italic;'>Cash and Debt Management</p>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["FoC pending", "FoC in pipeline"])

with tab1:
  uploaded_file = st.file_uploader("Upload Ceiling Pending file"
                                 , type = ['xlsx']
                                )

  st.header("All FoC pending at Finance")
  try:
    st.dataframe(all_pending(uploaded_file))
  except ValueError:
    st.write("*Upload file to generate report* :scroll:")

  st.header("FoC pending at Finance (at Senior Most level)")
  try:
    st.dataframe(seniormost(uploaded_file))
  except ValueError:
    st.write("*Upload file to generate report* :scroll:")

  st.header("CSS & TG-CFC details")
  try:
    st.dataframe(css_ss(uploaded_file))
  except ValueError:
    st.write("*Upload file to generate report* :scroll:")
  except:
    st.write("*No CSS or TG-CFC FoC pending right now*")

  st.header("SOPD-SS details")
  try:
    st.dataframe(sopd_ss(uploaded_file))
  except ValueError:
    st.write("*Upload file to generate report* :scroll:")
  except:
    st.write("*No SOPD-SS FoC pending right now*")


with tab2:
  uploaded_file_approved = st.file_uploader("Upload Ceiling Approved file"
                                 , type = ['xlsx']
                                )

  uploaded_file_foc_exp = st.file_uploader("Upload FoC expenditure bill wise file"
                                 , type = ['csv']
                                )
  st.header("FoC in pipeline")
  if uploaded_file_approved is None or uploaded_file_foc_exp is None:
        st.info("Please upload **both** files to generate the report.")
  else:
          try:
                  df1, df2 = pipeline(uploaded_file_approved, uploaded_file_foc_exp)
                  st.dataframe(df1)
                  st.download_button(
                  label="⬇️ Download CSV",
                  data=df2,
                  file_name="foc_pipeline.csv",
                  mime="text/csv",
          )
          except Exception as e:
                  st.error(f"Could not generate report: {e}")
          
