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
   
    data_uno = [
       {"Start": dt.datetime(2023, 1, 25, 10, 15, 1), "Finish": dt.datetime(2023, 1, 25, 10, 17, 30), "Final_Value": 0.7},
       {"Start": dt.datetime(2023, 1, 25, 10, 18, 20), "Finish": dt.datetime(2023, 1, 25, 10, 20, 40), "Final_Value": 0.75},
       {"Start": dt.datetime(2023, 1, 25, 10, 22, 5), "Finish": dt.datetime(2023, 1, 25, 10, 23, 15), "Final_Value": 0.88},
       {"Start": dt.datetime(2023, 1, 25, 10, 23, 30), "Finish": dt.datetime(2023, 1, 25, 10, 25, 10), "Final_Value": 0.8},
       {"Start": dt.datetime(2023, 1, 25, 10, 27, 12), "Finish": dt.datetime(2023, 1, 25, 10, 28, 19), "Final_Value": 0.74},
       {"Start": dt.datetime(2023, 1, 25, 10, 29, 44), "Finish": dt.datetime(2023, 1, 25, 10, 33, 11), "Final_Value": 0.69},
       {"Start": dt.datetime(2023, 1, 25, 10, 35, 25), "Finish": dt.datetime(2023, 1, 25, 10, 38, 55), "Final_Value": 0.6},
    ]

    # Create a DataFrame from data_uno with the corrected variable name
    df_final_values = pd.DataFrame(data_uno, columns=['Start', 'Finish', 'Final_Value'])

    # Plotting Gantt chart with color denoting final values
    fig2 = px.timeline(df_final_values, x_start="Start", x_end="Finish", y="Final_Value")
    fig2.update_layout(title_text='Gantt Chart with Final Values')
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
    st.write(checkdata[0][1], checkdata[0][2], checkdata[0][3])

    example_data = []
    x = dt.datetime(2023, 1, 25, 10, 15, 1)
    z = dt.datetime(2023, 1, 25, 10, 17, 30)
    v = 0.7
    example_data.append({"Start": data_uno[0]["Start"], "Finish": data_uno[0]["Finish"], "Final_Value": data_uno[0]["Final_Value"]})
    st.write(example_data)

    example_data_carrier = pd.DataFrame(example_data)
    fig = px.timeline(example_data, x_start="Start", x_end="Finish", y="Final_Value", title="Gantt Chart Example")
    st.plotly_chart(fig)
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
