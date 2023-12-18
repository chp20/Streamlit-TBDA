import streamlit as st
import datetime as dt
import mysql.connector
import plotly.express as px
import pandas as pd

points = [
    (dt.datetime(2023, 1, 25, 10, 18, 20), 500, 550, 570, 1000, 1200, 1100, 100, 90, 60, 0.6, 0.65, 0.77),
    (dt.datetime(2023, 1, 25, 10, 19, 40), 640, 720, 430, 970, 1040, 890, 30, 56, 77, 0.36, 0.78, 0.76),
    (dt.datetime(2023, 1, 25, 10, 20, 40), 600, 780, 400, 990, 1050, 850, 50, 66, 67, 0.66, 0.68, 0.73)
]

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

    st.subheader("Plots of First Three, Second Three, Third Three, and Fourth Three Sets")

    # Function to create Plotly Express plots
    def create_plotly_express_plots(points):
        num_plots = len(points) // 3  # Adjust this based on your requirement

        for i in range(num_plots):
            start_index = i * 3
            end_index = (i + 1) * 3
            subset = points[start_index:end_index]

            # Extracting datetime and y values
            datetimes, *y_values = zip(*subset)

            # Creating plot
            st.subheader(f'Plot {i + 1}')
            df = pd.DataFrame({'Datetime': datetimes, 'Set 1': y_values[0], 'Set 2': y_values[1], 'Set 3': y_values[2]})
            fig = px.line(df, x='Datetime', y=['Set 1', 'Set 2', 'Set 3'], markers=True)
            st.plotly_chart(fig)

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
