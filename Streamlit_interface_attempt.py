#import modules, make sure to pip install these modules on your pc since you will be downloading this code
import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
from influxdb_client import InfluxDBClient
import mysql.connector
import matplotlib.pyplot as plt

boolean_decision = st.checkbox('Allow me to enter final dates')

if boolean_decision:
    # If checkbox is checked, show the final date inputs
    final_col1, final_col2 = st.columns(2)
    
    with final_col1:
        with st.expander('Definitive begin date'):
            final_begin_date = st.date_input('Give your begin date:', key="final_begin_date")
            final_begin_time = st.time_input('Begin time:', key="final_begin_time")
            
    with final_col2:
        with st.expander('Definitive final date'):
            final_end_date = st.date_input('Give your final date:', key="final_end_date")
            final_end_time = st.time_input('Final time:', key="final_end_time")
    
    final_date_begin = dt.datetime.combine(final_begin_date, final_begin_time)
    final_date_end = dt.datetime.combine(final_end_date, final_end_time)
else:
    # If checkbox is not checked, create an empty placeholder
    placeholder = st.empty()
    col1, col2, col3 = st.columns(3)
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
    qry = "select * FROM `actividad-G02`"
    mycursor.execute(qry)
    rows = mycursor.fetchall()
    df = []
    for x in rows:
        if x[4] > date_begin and x[5] < date_end:
            #st.write(x[4])
            df.append((x[4],x[5]))
    
    connection.commit()
    mycursor.close()
    connection.close()
    
        
    i = 0
    check = []
    for i in df:
        check.append(i)
    fig, ax = plt.subplots()
    plot = ax.plot_date(check, np.ones(len(df)))
    plt.xticks(fontsize=5)
    
    # Pass the Matplotlib figure (fig) to st.pyplot
    st.pyplot(fig)




