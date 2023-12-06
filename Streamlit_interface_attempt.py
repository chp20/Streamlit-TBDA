#import modules, make sure to pip install these modules on your pc since you will be downloading this code
import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
from influxdb_client import InfluxDBClient
import mysql.connector
#make it more fancy
col1, col2, col3 = st.columns(3)

#create time inputs
with col1:
    with st.expander('Begin date'):
        begin_date = st.date_input('Give your begin date:')
        begin_time = st.time_input('Begin time:')

with col2:
    with st.expander('Final date'):
        Final_date = st.date_input('Give your final date:')
        Final_time = st.time_input('Final time:')

#create boxes to let viewer choose what values he wants to see
with col3:
    with st.expander('Values to be plotted'):
        S_bool = st.checkbox('S_Values')
        a_bool = st.checkbox('a_values')
        g_bool = st.checkbox('g_values')
        m_bool = st.checkbox('m_values')

        
#create time intervals
date_begin = dt.datetime.combine(begin_date, begin_time)
date_end = dt.datetime.combine(Final_date, Final_time)
interval_max = dt.timedelta(days=10)
time_difference = date_end - date_begin

#create boolean check for time interval chosen
if time_difference > interval_max:
    st.write('Its not possible to select more than 11 days.')

# def get_influx(mac, auth, dat, time_window):
#     dat['From'] = dat.desde.dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
#     dat['To']   = dat.hasta.dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    
#    #|> filter(fn: (r) => r._field == "Gx" or r._field == "Gy" or r._field == "Gz" ) \
    
#     query =  'from(bucket: "SSL/autogen") \
#           |> range(start: '+ dat.loc[0,'From'] + ', stop: '+ dat.loc[0,'To'] + ') \
#           |> filter(fn: (r) => r["_measurement"] == "sensoria_socks") \
#           |> filter(fn: (r) => r._field == "S0" or r._field == "S1" or r._field == "S2" or r._field == "Gx" or r._field == "Gy" or r._field == "Gz" or r._field == "Ax" or r._field == "Ay" or r._field == "Az"  )\
#           |> filter(fn: (r) => r["mac"] == "' + mac + '") \
#           |> group(columns: ["_field","lat","lng"]) \
#           |> drop(columns: ["table", "_start", "_stop","lat","lng"]) \
#           |> aggregateWindow(every: '+time_window+', fn: mean) \
#           |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value") \
#     '
    

#     clnt = InfluxDBClient(url=auth['url'],\
#                 token=auth['token'],org=auth['org'], timeout= 5000000)
#     result = clnt.query_api().query(org=auth['org'], query=query)
#     res    = pd.DataFrame()
#     for i in result:
#         rs = []
#         for row in i.records:
#             rs.append(row.values)
#         res= pd.concat([res,pd.DataFrame(rs)],axis=0)
#     if res.shape[0] > 0:
#         res    = res.drop(res.columns[[0]],axis=1)
#         #msk = ( res['Gx'].isnull() & res['Gy'].isnull() & res['Gz'].isnull() )
#         msk = ( res['Gx'].isnull() & res['Gy'].isnull() & res['Gz'].isnull() & res['S0'].isnull() & res['S1'].isnull() & res['S2'].isnull() & res['Ax'].isnull() & res['Ay'].isnull()& res['Az'].isnull())
#         idx = res.index[msk]
#         res = res.drop(index=idx)
#         res = res.drop(res.columns[[0]],axis=1) # drop Table column
#         res.sort_values(by='_time',ascending=True,inplace=True)
#         #res.eval("Gmag = sqrt(Gx**2 + Gy**2 + Gz**2)", engine='numexpr', inplace=True)
#         #res.eval("Gmag = sqrt(gx**2 + gy**2 + gz**2)", engine='numexpr', inplace=True)
#         res.reset_index(drop=True,inplace=True)
#         res['desde'] = res['_time'] + pd.Timedelta(hours=-1)
#         pd.options.display.max_columns = 0
#     clnt.close()
#     return({'qry':query,'res':res})
# #

# auth = {}
# auth['org']  = 'UPM'    
# auth['token']= 'HcxJ7OEkZJbvoYdXfZPUT6to6xsO-XgVT-u-Mj21U_MiFX4PIsCyFQbGUDwEDICvdko2PnTTUE4XjiQdT4g5Hg=='
# auth['url']  = 'https://apiivm78.etsii.upm.es:8086'

# #date_first = pd.DataFrame([{'desde':'2023-05-01 00:00:00.000','hasta':'2023-10-08 23:59:59.999','name':'PAT1','set':'S-04'},{'desde':'2023-05-01 00:00:00.000','hasta':'2023-10-08 23:59:59.999','name':'PAT2','set':'S-04'}])
# date_first = pd.DataFrame([{'desde':'2023-01-01 00:00:00.000','hasta':'2023-01-28 23:59:59.999','name':'PAT1','set':'S-04'}])
 
# left_sock = 'E0:52:B2:8B:2A:C2'
# right_sock =  'C9:7B:84:76:32:14'

# date_first['desde'] = pd.to_datetime(date_first['desde'])
# date_first['hasta'] = pd.to_datetime(date_first['hasta'])

# res1 = get_influx( mac = left_sock , auth = auth, dat = date_first, time_window = '1m') 
#st.write(res1)

connection = mysql.connector.connect(
    host = "apiivm78.etsii.upm.es", 
    user = "TBDA",
    password = "UPM#2324",
    database="sclerosisTBDA"
    )



mycursor = connection.cursor()
qry = "select * FROM `actividad-G02`"
mycursor.execute(qry)
rows = mycursor.fetchall()
df = []
for x in rows:
    if x[4] > date_begin and x[5] < date_end:
        #st.write(x[4])
        df.append(x)
    #else:
     #   st.write('no')
        
st.write(df)
connection.commit()
mycursor.close()
connection.close()
