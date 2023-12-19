import streamlit as st
with st.expander('Values to be plotted'):
    S_bool = st.checkbox('S_Values')
    a_bool = st.checkbox('a_values')
    g_bool = st.checkbox('g_values')
    m_bool = st.checkbox('m_values')

if S_bool:
    st.write('Sbool')
if a_bool:
    st.write('abool')
if g_bool:
    st.write('gbool')
if m_bool:
    st.write('mbool')
