import streamlit as st

from word.state_word import USER_STATE

def show():
    user = st.session_state.get(USER_STATE)
    st.title("ダッシュボード")
    if user:
        st.write(f"こんにちは、{user.name}さん")
    else:
        st.error("ユーザー情報がありません")