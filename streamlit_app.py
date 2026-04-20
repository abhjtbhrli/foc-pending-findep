import streamlit as st
import pandas as pd
import numpy as np
from google.oauth2.service_account import Credentials
import gspread
import excl as e

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
  pend['DEPARTMENT NAME2'] = np.where(pend['DEPARTMENT NAME'].isin(e.PWD), 'PWD', 'Non PWD')
    
  pend['SCHEME NAME2'] = np.where(pend['SCHEME CODE'].isin(e.CSS_list),
                                'CSS',
                                np.where(pend['SCHEME CODE'].isin(e.EAP_list),
                                         'EAP',
                                         np.where(pend['SCHEME CODE'].isin(e.NIDA_list),
                                                  'NIDA',
                                                  np.where(pend['SCHEME CODE'].isin(e.RIDF_list),
                                                                                    'RIDF',
                                                                                    np.where(pend['SCHEME CODE'].isin(e.SOPD_list),
                                                                                             'SOPD',
                                                                                             np.where(pend['SCHEME CODE'].isin(e.TG_list),
                                                                                                      'TG',
                                                                                                      np.where(pend['SCHEME CODE']=='EE',
                                                                                                               'EE',
                                                                                                               np.where(pend['SCHEME CODE'].isin(e.UIDF_list),
                                                                                                                        'UIDF',
                                                                                                                        np.where(pend['SCHEME CODE'].isin(e.SCDF_list),
                                                                                                                                 'SCDF',
                                                                                                                                 pend['SCHEME CODE'])))))))))
  
  pend['MH'] = pend['HEAD OF ACCOUNT'].str.slice(0,4)
  pend['MH'] = pd.to_numeric(pend['MH'])
  pend['Rev-Cap'] = np.where((pend['MH']<3999) & (pend['MH']>=2000),
                           'Revenue',
                           np.where((pend['MH']<5999) & (pend['MH']>=4000),
                                    'Capital',
                                    'Loans & Advances'))
  
  pend['Hierarchy'] = np.where(pend['HELD BY'].isin(e.SENIORMOST_list), 'Seniormost', 'Non Seniormost')
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
  try:
    df3.fillna('', inplace=True)
    return df3
  except:
    return df3

def seniormost(file):
  import pandas as pd
  import numpy as np

  pend = pd.read_excel(file, engine = "openpyxl")
  pend.columns = pend.iloc[0].tolist()
  pend = pend[2:]
  pend['DEPARTMENT NAME2'] = np.where(pend['DEPARTMENT NAME'].isin(e.PWD), 'PWD', 'Non PWD')
  pend['MH'] = pend['HEAD OF ACCOUNT'].str.slice(0,4)
  pend['MH'] = pd.to_numeric(pend['MH'])
  pend['Rev-Cap'] = np.where((pend['MH']<3999) & (pend['MH']>=2000),
                           'Revenue',
                           np.where((pend['MH']<5999) & (pend['MH']>=4000),
                                    'Capital',
                                    'Loans & Advances'))
  pend['SCHEME NAME2'] = np.where(pend['SCHEME CODE'].isin(e.CSS_list),
                                'CSS',
                                np.where(pend['SCHEME CODE'].isin(e.EAP_list),
                                         'EAP',
                                         np.where(pend['SCHEME CODE'].isin(e.NIDA_list),
                                                  'NIDA',
                                                  np.where(pend['SCHEME CODE'].isin(e.RIDF_list),
                                                                                    'RIDF',
                                                                                    np.where(pend['SCHEME CODE'].isin(e.SOPD_list),
                                                                                             'SOPD-G, TG',
                                                                                             np.where(pend['SCHEME CODE'].isin(e.TG_list),
                                                                                                      'TG Central FC',
                                                                                                      np.where(pend['SCHEME CODE']=='EE',
                                                                                                               'EE',
                                                                                                               np.where(pend['SCHEME CODE'].isin(e.UIDF_list),
                                                                                                                        'UIDF',
                                                                                                                        np.where(pend['SCHEME CODE'].isin(e.SCDF_list),
                                                                                                                                 'SCDF',
                                                                                                                                 pend['SCHEME CODE'])))))))))
  
  pend['MH'] = pend['HEAD OF ACCOUNT'].str.slice(0,4)
  pend['MH'] = pd.to_numeric(pend['MH'])
  pend['Rev-Cap'] = np.where((pend['MH']<3999) & (pend['MH']>=2000),
                           'Revenue',
                           np.where((pend['MH']<5999) & (pend['MH']>=4000),
                                    'Capital',
                                    'Loans & Advances'))
  
  pend['Hierarchy'] = np.where(pend['HELD BY'].isin(e.SENIORMOST_list), 'Seniormost', 'Non Seniormost')
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
  css_df = css_df[css_df['SCHEME CODE'].isin(['CSS', 'TG-CFC', 'TG-FFC'])]
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
  pipe['HEAD OF ACCOUNT'] = pipe['HEAD OF ACCOUNT'].astype(str).str.strip()
  pipe['DH'] = pipe['HEAD OF ACCOUNT'].str[-5:]
  pipe = pipe[pipe['DH'].isin(['36-00'])==False]
  pipe['MH'] = pipe['HEAD OF ACCOUNT'].str[:1]
  pipe['ISSUED ON'] = pd.to_datetime(pipe['ISSUED ON'])
  today = pd.to_datetime("today").normalize()
  pipe["Days"] = (today - pipe["ISSUED ON"]).dt.days
  excl = e.EXCL

  

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

  
  pipe['SCHEME CODE2'] = np.where(pipe['SCHEME CODE'].isin(e.SOPD_list),
                                   'SOPD-G, TG',
                                   np.where(pipe['SCHEME CODE'].isin(e.RIDF_list),
                                            'RIDF',
                                            np.where(pipe['SCHEME CODE'].isin(e.TG_list),
                                                     'TG Central FC',
                                                     np.where((pipe['SCHEME CODE'].isin(e.CSS_list)) & (pipe['DH'][0:2]!='31'),
                                                              'CSS',
                                                              np.where(pipe['SCHEME CODE'].isin(e.EAP_list),
                                                                       'EAP',
                                                                       np.where(pipe['SCHEME CODE'].isin(e.NIDA_list),
                                                                                'NIDA',
                                                                                np.where(pipe['SCHEME CODE'].isin(e.UIDF_list),
                                                                                         'UIDF',
                                                                                         np.where(pipe['SCHEME CODE'].isin(e.SCDF_list),
                                                                                                  'SCDF',
                                                                                                  np.where((pipe['SCHEME CODE']=='EE') & (pipe['DH'][0:2]!='31'),
                                                                                                           'EE',
                                                                                                           np.where((pipe['SCHEME CODE']=='EE') & (pipe['DH'][0:2]=='31'),
                                                                                                                    'EE Salary',
                                                                                                                    np.where((pipe['SCHEME CODE'].isin(e.CSS_list)) & (pipe['DH'][0:2]=='31'),
                                                                                                                             'CSS Salary',
                                                                                                                             pipe['SCHEME CODE'])))))))))))
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
  pipex = pipex[pipex['DH']!='36-00'] 
  csv = pipe[(pipe['Days']<=15) & (pipe['Exp']=='No') & (pipe['Excl']=='No') & (pipe['DH']!='36-00')].to_csv(index=False).encode("utf-8")
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
          
