import streamlit as st
import datetime as dt 
import pandas as pd
import plotly.express as px

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


with st.expander('Values to be plotted'):
        S_bool = st.checkbox('S_Values')
        a_bool = st.checkbox('a_values')
        g_bool = st.checkbox('g_values')
        m_bool = st.checkbox('m_values')

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
