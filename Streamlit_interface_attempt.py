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

connection = mysql.connector.connect(
    host = "apiivm78.etsii.upm.es", 
    user = "TBDA",
    password = "UPM#2324",
    database="sclerosisTBDA"
    )

mycursor = connection.cursor()
mycursor.execute("SHOW TABLES")
for x in mycursor:
    st.write(x)
connection.commit()
mycursor.close()
connection.close()
