# routing/routing.py
import streamlit as st
from logic.top_logic import get_user
from page.top_page import show as top
from page.dashboard_page import show as dashboard
from page.record_page import show as record
from page.analysis_page import show as analysis


MENU = "メニュー"
DASHBOARD = "利用中のガット一覧"
RECORD = "ガット登録"
ANALYSIS = "過去ガットの分析"
MENU_ITEM = [DASHBOARD, RECORD, ANALYSIS]
USER_STATE = "user"
TOKEN_STATE = "token"

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
    menu = st.sidebar.selectbox(MENU,MENU_ITEM)
    pages = {
        DASHBOARD: dashboard,
        RECORD: record,
        ANALYSIS: analysis,
    }
    pages.get(menu, dashboard)()