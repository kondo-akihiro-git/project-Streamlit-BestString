# page/dashboard_page.py
import streamlit as st
from streamlit_elements import elements, mui

from logic.dashboard_logic import get_records
from word.state_word import USER_STATE


def show():
    user = st.session_state.get(USER_STATE)

    st.title("ダッシュボード")

    if not user:
        st.error("ユーザー情報がありません")
        return

    records = get_records(user.id)

    if not records:
        st.info("まだ記録がありません")
        return

    # -----------------------
    # ガット表示
    # -----------------------

    with elements("dashboard"):
        with mui.Grid(container=True, spacing=2):
            for r in records:
                with mui.Grid(item=True, xs=12, sm=6):
                    with mui.Card():
                        with mui.CardContent():
                            vertical = r["vertical_strand"]
                            horizontal = r["horizontal_strand"]

                            if vertical == horizontal:
                                mui.Typography(
                                    f"{vertical}",
                                    variant="body2",
                                )
                            else:
                                mui.Typography(
                                    f"縦ガット: {vertical}",
                                    variant="body2",
                                )
                                mui.Typography(
                                    f"横ガット: {horizontal}",
                                    variant="body2",
                                )
                            with mui.Box(
                                sx={
                                    "backgroundImage": (f"url({r['vertical_image']})"),
                                    "backgroundRepeat": "no-repeat",
                                    "backgroundPosition": "center",
                                    "backgroundSize": "auto 100%",
                                    "minHeight": 180,
                                }
                            ):
                                pass

                            mui.Divider()
                            mui.Typography(f"ラケット: {r['racket']}",variant="body2")
                            mui.Typography(f"張った日: {r['set_date']}",variant="body2")