import streamlit as st

params = st.query_params
isPing = params.get("p") == "1"

if isPing:
    st.write("pong")
    st.stop()
