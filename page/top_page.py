# page/top_page.py
import streamlit as st
from logic.top_logic import create_url

def show():
    st.title("トップ画面")
    name = st.text_input("名前を入力してください")
    st.write("ここでURLを発行する想定")
    if st.button("URL発行"):
        if not name:
            st.error("名前を入力してください")
            return
        url = create_url(name)
        st.success("URLを発行しました")
        st.code(url)