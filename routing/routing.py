# routing/routing.py
import streamlit as st
from logic.top_logic import get_user
from page.top_page import show as top
from page.dashboard_page import show as dashboard
from page.record_page import show as record
from page.analysis_page import show as analysis

# -----------------------
# ルーター本体
# -----------------------
def router():

    token = st.query_params.get("token")

    # -----------------------
    # ① トップ（tokenなし）
    # -----------------------
    if not token:
        top()
        return

    # -----------------------
    # ② tokenチェック
    # -----------------------
    user = get_user(token)

    if not user:
        st.query_params.clear()
        top()
        return

    # -----------------------
    # ③ ユーザー確定
    # -----------------------
    st.session_state["user"] = user

    # -----------------------
    # ④ メニュー
    # -----------------------
    st.sidebar.title("メニュー")

    menu = st.radio("ページ", ["dashboard", "record", "analysis"])

    # -----------------------
    # ⑤ 画面表示
    # -----------------------
    if menu == "dashboard":
        dashboard()
    elif menu == "record":
        record()
    else:
        analysis()