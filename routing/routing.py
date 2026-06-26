import streamlit as st
from page.top_page import show as top
from page.dashboard_page import show as dashboard
from page.record_page import show as record
from page.analysis_page import show as analysis


def router():
    # URLパラメータ取得
    query = st.query_params
    page = query.get("page", None)

    # -----------------------
    # トップ
    # -----------------------
    if page is None:
        top()
        return

    # -----------------------
    # ルーティング
    # -----------------------
    st.sidebar.title("メニュー")

    if st.sidebar.button("dashboard"):
        st.query_params["page"] = "dashboard"
        st.rerun()

    if st.sidebar.button("record"):
        st.query_params["page"] = "record"
        st.rerun()

    if st.sidebar.button("analysis"):
        st.query_params["page"] = "analysis"
        st.rerun()

    # -----------------------
    # ページ分岐
    # -----------------------
    if page == "dashboard":
        dashboard()

    elif page == "record":
        record()

    elif page == "analysis":
        analysis()

    else:
        st.write("存在しないページです")
        top()