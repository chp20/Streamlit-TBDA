import streamlit as st
import datetime as dt
import mysql.connector
import plotly.express as px
import pandas as pd

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



    mycursor.close()
    connection.close()
st.write(rows)
