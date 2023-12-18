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
    
        ##plot it
        st.plotly_chart(fig2)



    ######################################################################################## Temporary workstation
    # # Sample data
    # x_values = np.array([1, 2, 3, 4, 5])
    # y_values = x_values ** 2  # Example: y = x^2
    
    # # Plotting the line graph
    # fig, ax = plt.subplots()
    # ax.plot(x_values, y_values, marker='o', linestyle='-', color='b', label='Data Points')
    
    # # Adding labels and title
    # ax.set_xlabel('X-axis Label')
    # ax.set_ylabel('Y-axis Label')
    # ax.set_title('Simple Line Graph')
    
    # # Adding legend
    # ax.legend()
    
    # # Display the plot using Streamlit
    # st.pyplot(fig)
    ###################################################################################### 


###########
###########    initial preliminary plotting
###########
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
            final_date = st.date_input('Give your final date:')
            final_time = st.time_input('Final time:')

    # Create boxes to let the viewer choose what values he wants to see
    with col3:
        with st.expander('Values to be plotted'):
            S_bool = st.checkbox('S_Values')
            a_bool = st.checkbox('a_values')
            g_bool = st.checkbox('g_values')
            m_bool = st.checkbox('m_values')

    # Create time intervals
    date_begin = dt.datetime.combine(begin_date, begin_time)
    date_end = dt.datetime.combine(final_date, final_time)
    interval_max = dt.timedelta(days=10)
    time_difference = date_end - date_begin

    # Create boolean check for the time interval chosen
    # if time_difference > interval_max:
    # st.write('It\'s not possible to select more than 11 days.')

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
            # Append a new dictionary to the list
            data.append({'datetime': x[4], 'time': x[5]})

    # Create a DataFrame from the list
    df = pd.DataFrame(data)

    # Check if the DataFrame is empty
    if df.empty:
        st.warning("No data available for the selected time range.")
    else:
        # Create a unitless y-axis column
        df['unitless_y'] = range(1, len(df) + 1)

        connection.commit()
        mycursor.close()
        connection.close()

        # Plotting with Plotly Express
        fig = px.scatter(df, x='datetime', y='unitless_y')

        # Remove y-axis label (optional)
        fig.update_yaxes(title_text='')

        # Display the Plotly Express chart
        st.plotly_chart(fig)
