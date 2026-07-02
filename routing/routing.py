# routing/routing.py
import streamlit as st
from streamlit_elements import elements, mui, sync
from logic.top_logic import get_user
from page.top_page import show as top
from page.dashboard_page import show as dashboard
from page.record_page import show as record
from page.analysis_page import show as analysis
from word.routing_word import ANALYSIS_BUTTON, ANALYSIS_PAGE, DASHBOARD_BUTTON, DASHBOARD_PAGE, RECORD_BUTTON, RECORD_PAGE
from word.state_word import PAGE_STATE, TOKEN_STATE, USER_STATE

# -----------------------
# ルーター本体
# -----------------------
def router():
    st.set_page_config(
        page_title="BestString",
        page_icon="🎾"
    )
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
    st.session_state[USER_STATE] = user

    # -----------------------
    # 初期値
    # -----------------------
    if st.session_state.get(PAGE_STATE) is None:
        st.session_state[PAGE_STATE] = DASHBOARD_PAGE

    col1, col2, col3 = st.columns(3)
    with col1:
        is_active = st.session_state[PAGE_STATE] == DASHBOARD_PAGE
        if st.button(DASHBOARD_BUTTON, use_container_width=True, type="primary" if is_active else "secondary"):
            st.session_state[PAGE_STATE] = DASHBOARD_PAGE
            st.rerun()

    with col2:
        is_active = st.session_state[PAGE_STATE] == RECORD_PAGE
        if st.button(RECORD_BUTTON, use_container_width=True, type="primary" if is_active else "secondary"):
            st.session_state[PAGE_STATE] = RECORD_PAGE
            st.rerun()

    with col3:
        is_active = st.session_state[PAGE_STATE] == ANALYSIS_PAGE
        if st.button(ANALYSIS_BUTTON, use_container_width=True, type="primary" if is_active else "secondary"):
            st.session_state[PAGE_STATE] = ANALYSIS_PAGE
            st.rerun()

    # -----------------------
    # ルーティング
    # -----------------------
    if st.session_state[PAGE_STATE] == DASHBOARD_PAGE:
        dashboard()
    elif st.session_state[PAGE_STATE] == RECORD_PAGE:
        record()
    elif st.session_state[PAGE_STATE] == ANALYSIS_PAGE:
        analysis()