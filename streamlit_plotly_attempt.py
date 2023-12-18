import streamlit as st
import datetime as dt
import mysql.connector
import plotly.express as px
import pandas as pd

# Streamlit UI
st.title('Interactive Plots with Streamlit')

boolean_decision = st.checkbox('Allow me to enter final dates')

if boolean_decision:
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

    connection = mysql.connector.connect(
        host="apiivm78.etsii.upm.es",
        user="TBDA",
        password="UPM#2324",
        database="sclerosisTBDA"
    )

    checkdata = []
    mycursor = connection.cursor()
    qry = "select * FROM `Data_sample_Christian`"
    mycursor.execute(qry)
    rows = mycursor.fetchall()

    for x in rows:
        if final_date_begin <= x[1] and final_date_end >= x[2]:
            checkdata.append(x)

    mycursor.close()
    connection.close()

    ticker = 0
    checkdata_carrier = []

    while ticker < len(checkdata):
        checkdata_carrier.append({"Start": checkdata[ticker][1], "Finish": checkdata[ticker][2],
                                  "Final_Value": checkdata[ticker][3]})
        ticker += 1

    carrierdf = pd.DataFrame(checkdata_carrier)

    if carrierdf.empty:
        st.warning("No data available for the selected time range.")
    else:
        fig2 = px.timeline(carrierdf, x_start="Start", x_end="Finish", y="Final_Value", color="Final_Value",
                           color_continuous_scale=[(0, "red"), (1, "green")])
        fig2.update_layout(title_text='Gantt Chart with Final Values')
        st.plotly_chart(fig2)

    
    points = [
        (dt.datetime(2023, 1, 25, 10, 18, 20), 500, 550, 570, 1000, 1200, 1100, 100, 90, 60, 0.6, 0.65, 0.77),
        (dt.datetime(2023, 1, 25, 10, 19, 40), 640, 720, 430, 970, 1040, 890, 30, 56, 77, 0.36, 0.78, 0.76),
        (dt.datetime(2023, 1, 25, 10, 20, 40), 600, 780, 400, 990, 1050, 850, 50, 66, 67, 0.66, 0.68, 0.73)
    ]
    
    gnull = []
    gone = []
    gtwo = []
    mnull = []
    mone = []
    mtwo = []
    snull=[]
    sone=[]
    stwo=[]
    anull = []
    aone = []
    atwo = []

    i = 0
    while i < len(points):
        gnull.append(points[i][1])
        gone.append(points[i][2])
        gtwo.append(points[i][3])
        mnull.append(points[i][4])
        mone.append(points[i][5])
        mtwo.append(points[i][6])
        snull.append(points[i][7])
        sone.append(points[i][8])
        stwo.append(points[i][9])
        anull.append(points[i][10])
        aone.append(points[i][11])
        atwo.append(points[i][12])
        i+=1
    st.write(gnull,gone,gtwo)

else:
    placeholder = st.empty()
    col1, col2, col3 = st.columns(3)

    with col1:
        with st.expander('Begin date'):
            begin_date = st.date_input('Give your begin date:')
            begin_time = st.time_input('Begin time:')

    with col2:
        with st.expander('Final date'):
            final_date = st.date_input('Give your final date:')
            final_time = st.time_input('Final time:')

    with col3:
        with st.expander('Values to be plotted'):
            S_bool = st.checkbox('S_Values')
            a_bool = st.checkbox('a_values')
            g_bool = st.checkbox('g_values')
            m_bool = st.checkbox('m_values')

    date_begin = dt.datetime.combine(begin_date, begin_time)
    date_end = dt.datetime.combine(final_date, final_time)
    interval_max = dt.timedelta(days=10)
    time_difference = date_end - date_begin

    connection = mysql.connector.connect(
        host="apiivm78.etsii.upm.es",
        user="TBDA",
        password="UPM#2324",
        database="sclerosisTBDA"
    )

    mycursor = connection.cursor()
    qry = "select * FROM `actividad-G02`"
    mycursor.execute(qry)
    rows = mycursor.fetchall()

    data = []

    for x in rows:
        if date_begin <= x[4] <= date_end:
            data.append({'datetime': x[4], 'time': x[5]})

    df = pd.DataFrame(data)

    if df.empty:
        st.warning("No data available for the selected time range.")
    else:
        df['unitless_y'] = range(1, len(df) + 1)
        connection.commit()
        mycursor.close()
        connection.close()
        fig = px.scatter(df, x='datetime', y='unitless_y')
        fig.update_yaxes(title_text='')
        st.plotly_chart(fig)
