# routing/routing.py
import streamlit as st
from logic.top_logic import get_user
from page.top_page import show as top
from page.dashboard_page import show as dashboard
from page.record_page import show as record
from page.analysis_page import show as analysis
from word.routing_word import ANALYSIS, DASHBOARD, MENU, RECORD
from word.state_word import TOKEN_STATE, USER_STATE

# -----------------------
# ルーター本体
# -----------------------
def router():
    # -----------------------
    # ① token無しはトップ遷移
    # -----------------------
    token = st.query_params.get(TOKEN_STATE)
    if not token:
        top()
        return

    # -----------------------
    # ② ユーザー無しはトップ遷移
    # -----------------------
    user = get_user(token)
    if not user:
        st.query_params.clear()
        top()
        return

    # -----------------------
    # ③ ユーザー有りはメニュー遷移
    # -----------------------
    st.session_state[USER_STATE] = user
    tab1, tab2, tab3 = st.tabs([DASHBOARD, RECORD, ANALYSIS])
    with tab1:
        dashboard()
    with tab2:
        record()
    with tab3:
        analysis()