import streamlit as st

def show():
    user = st.session_state.get("user")
    st.title("ダッシュボード")
    if user:
        st.write(f"こんにちは、{user.name}さん")
    else:
        st.error("ユーザー情報がありません")