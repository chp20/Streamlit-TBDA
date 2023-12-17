import streamlit as st

# Your Streamlit app code

# Example: Embedding Grafana iframe
grafana_iframe_code = """<iframe src="https://apiict00.etsii.upm.es/grafana/d-solo/cqDSTooVk/socks_set4?orgId=3&from=1674623850987&to=1674674296888&panelId=10" width="100%" height="400" frameborder="0"></iframe>"""

st.markdown(grafana_iframe_code, unsafe_allow_html=True)

# Rest of your Streamlit app code
