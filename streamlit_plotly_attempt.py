##Import modules
import streamlit as st
import pandas as pd
import datetime as dt
import mysql.connector
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np

##create switch between initial testing and final dates
boolean_decision = st.checkbox('Allow me to enter final dates')

##first the final dates part
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

    ##final datetime format chosen dates
    final_date_begin = dt.datetime.combine(final_begin_date, final_begin_time)
    final_date_end = dt.datetime.combine(final_end_date, final_end_time)

    ##connect to mariadb --> phpmyadmin
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

    ##collect all data within timeframe given by user
    for x in rows:
        if final_date_begin <= x[1] and final_date_end >= x[2]:
            checkdata.append(x)

    mycursor.close()
    connection.close()

    ##append relevant part of data to new list
    ticker = 0
    checkdata_carrier = []

    ##Set up the plot and add data to right format
    while ticker < len(checkdata):
        checkdata_carrier.append({"Start": checkdata[ticker][1], "Finish": checkdata[ticker][2], "Final_Value": checkdata[ticker][3]})
        ticker += 1
    carrierdf = pd.DataFrame(checkdata_carrier)

    if carrierdf.empty:
        st.warning("No data available for the selected time range.")
    else:
        fig2 = px.timeline(carrierdf, x_start="Start", x_end="Finish", y="Final_Value", color="Final_Value",
                           color_continuous_scale=[(0, "red"), (1, "green")])
        fig2.update_layout(title_text='Gantt Chart with Final Values')

        # plot the Gantt chart
        st.plotly_chart(fig2)

        # Iterate through each data point and create a subplot for each
        for index, row in carrierdf.iterrows():
            with st.expander(f'Data Point {index+1}'):
                # Filter data within the time window of the current data point
                sub_data = checkdata[(checkdata[:, 1] >= row['Start']) & (checkdata[:, 2] <= row['Finish'])]

                # Plot subplots
                for sub_index, sub_row in enumerate(sub_data):
                    plt.figure(figsize=(8, 4))
                    plt.plot(sub_row[4], sub_row[5], marker='o', linestyle='-', color='b', label='Data Points')
                    plt.xlabel('X-axis Label')
                    plt.ylabel('Y-axis Label')
                    plt.title(f'Subplot for Data Point {index+1} - Subplot {sub_index+1}')
                    plt.legend()

                    # Display the subplot using Streamlit
                    st.pyplot(plt.gcf())
