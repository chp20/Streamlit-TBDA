import streamlit as st
import pandas as pd
import datetime as dt
import mysql.connector
import plotly.express as px

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
   
    data = [
    dict("datetime.datetime(2023, 1, 25, 10, 15, 1)", "datetime.datetime(2023, 1, 25, 10, 17, 30)", 0.7),
    dict( "datetime.datetime(2023, 1, 25, 10, 18, 20)", "datetime.datetime(2023, 1, 25, 10, 20, 40)", 0.75),
    dict( "datetime.datetime(2023, 1, 25, 10, 22, 5)", "datetime.datetime(2023, 1, 25, 10, 23, 15)", 0.88),
    dict( "datetime.datetime(2023, 1, 25, 10, 23, 30)", "datetime.datetime(2023, 1, 25, 10, 25, 10)", 0.8),
    dict( "datetime.datetime(2023, 1, 25, 10, 27, 12)", "datetime.datetime(2023, 1, 25, 10, 28, 19)", 0.74),
    dict( "datetime.datetime(2023, 1, 25, 10, 29, 44)", "datetime.datetime(2023, 1, 25, 10, 33, 11)", 0.69),
    dict( "datetime.datetime(2023, 1, 25, 10, 35, 25)", "datetime.datetime(2023, 1, 25, 10, 38, 55)", 0.6),
]
 

    
    fig2 = px.timeline(data, x_start="Start", x_end="Finish", y="Task")
    fig2.update_layout(title_text='Gantt Chart with Links')
    st.plotly_chart(fig2)
    
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
        checkdata.append(x)
    mycursor.close()
    connection.close()

    
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
    #if time_difference > interval_max:
    #st.write('It\'s not possible to select more than 11 days.')

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
    
    
