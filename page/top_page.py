# page/top_page.py
import streamlit as st
from logic.top_logic import create_url

def show():
    st.title("トップ画面")

    st.write("ここでURLを発行する想定")

    if st.button("URL発行"):
        url = create_url()
        st.success("URLを発行しました")
        st.code(url)