import streamlit as st

def show():
    st.title("トップ画面")

    st.write("ここでURLを発行する想定")

    if st.button("アプリ開始"):
        st.query_params["page"] = "dashboard"
        st.rerun()