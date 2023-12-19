import streamlit as st
import datetime as dt
import pandas as pd
import plotly.express as px

final_date_begin_values = None
final_date_end_values = None

m_bool = False
g_bool = False
S_bool = False
a_bool = False

boolean_decision2 = st.checkbox('Allow me to enter final dates for dataplot')

if boolean_decision2:
    final_col1, final_col2 = st.columns(2)
    with final_col1:
        with st.expander('Definitive begin date'):
            final_begin_date_values = st.date_input('Give your begin date final values:', key="final_begin_date_values")
            final_begin_time_values = st.time_input('Begin time final values:', key="final_begin_time_values")

    with final_col2:
        with st.expander('Definitive final date'):
            final_end_date_values = st.date_input('Give your final date:', key="final_end_date_values")
            final_end_time_values = st.time_input('Final time:', key="final_end_time_values")

    final_date_begin_values = dt.datetime.combine(final_begin_date_values, final_begin_time_values)
    final_date_end_values = dt.datetime.combine(final_end_date_values, final_end_time_values)

    boolean_decision3 = st.checkbox('plot the following data')
    if boolean_decision3:
        with st.expander('Values to be plotted'):
            S_bool = st.checkbox('S_Values')
            a_bool = st.checkbox('a_values')
            g_bool = st.checkbox('g_values')
            m_bool = st.checkbox('m_values')

# Sample data points
points1 = [
    (dt.datetime(2023, 1, 25, 10, 18, 20), 500, 550, 570, 1000, 1200, 1100, 100, 90, 60, 0.6, 0.65, 0.77),
    (dt.datetime(2023, 1, 25, 10, 19, 40), 640, 720, 430, 970, 1040, 890, 30, 56, 77, 0.36, 0.78, 0.76),
    (dt.datetime(2023, 1, 25, 10, 20, 40), 600, 780, 400, 990, 1050, 850, 50, 66, 67, 0.66, 0.68, 0.73)
]

# Filter points based on final dates
points = [x for x in points1 if final_date_begin_values <= x[0] <= final_date_end_values]

# Extract data for plotting
if points:
    gnull, gone, gtwo, mnull, mone, mtwo, snull, sone, stwo, anull, aone, atwo = zip(*points)
    # Assuming all lists have the same length
    data = {
        'gnull': gnull,
        'gone': gone,
        'gtwo': gtwo,
        'mnull': mnull,
        'mone': mone,
        'mtwo': mtwo,
        'snull': snull,
        'sone': sone,
        'stwo': stwo,
        'anull': anull,
        'aone': aone,
        'atwo': atwo,
    }

    df = pd.DataFrame(data)

    # Streamlit app
    st.title('Database Plots')

    # Plotting function
    def plot_line_chart(dataframe, columns, title):
        fig = px.line(dataframe, x=dataframe.index, y=columns, labels={'index': 'Data Point', 'value': 'Value'})
        fig.update_layout(title=title)
        st.plotly_chart(fig)

    # Plot for gnull, gone, and gtwo
    if g_bool:
        st.subheader('Plot for gnull, gone, and gtwo')
        plot_line_chart(df[['gnull', 'gone', 'gtwo']], ['gnull', 'gone', 'gtwo'], 'gnull, gone, and gtwo Plot')

    # Plot for mnull, mone, and mtwo
    if m_bool:
        st.subheader('Plot for mnull, mone, and mtwo')
        plot_line_chart(df[['mnull', 'mone', 'mtwo']], ['mnull', 'mone', 'mtwo'], 'mnull, mone, and mtwo Plot')

    # Plot for snull, sone, and stwo
    if S_bool:
        st.subheader('Plot for snull, sone, and stwo')
        plot_line_chart(df[['snull', 'sone', 'stwo']], ['snull', 'sone', 'stwo'], 'snull, sone, and stwo Plot')

    # Plot for anull, aone, and atwo
    if a_bool:
        st.subheader('Plot for anull, aone, and atwo')
        plot_line_chart(df[['anull', 'aone', 'atwo']], ['anull', 'aone', 'atwo'], 'anull, aone, and atwo Plot')
else:
    st.warning("No data available for the selected date range.")
