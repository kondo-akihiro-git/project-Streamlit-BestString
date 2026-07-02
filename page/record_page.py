import streamlit as st
from datetime import date
from logic.record_logic import create_record, get_rackets, get_strands
from word.state_word import USER_STATE
from word.record_word import (
    PAGE_TITLE,
    NO_USER_ERROR,
    UNSELECTED_OPTION,
    RACKET_LABEL,
    VERTICAL_LABEL,
    HORIZONTAL_LABEL,
    SET_DATE_LABEL,
    BREAK_DATE_LABEL,
    TENSION_LABEL,
    COST_LABEL,
    MEMO_LABEL,
    RATING_LABEL,
    REGISTER_BUTTON_LABEL,
    REGISTER_SUCCESS_MSG,
    RACKET_REQUIRED_ERROR,
    VERTICAL_REQUIRED_ERROR,
    HORIZONTAL_REQUIRED_ERROR,
)


def show():
    st.title(PAGE_TITLE)

    user = st.session_state.get(USER_STATE)

    if not user:
        st.error(NO_USER_ERROR)
        return

    # -----------------------
    # DB取得
    # -----------------------
    rackets = get_rackets()
    strands = get_strands()

    racket_map = {r.name: r.id for r in rackets}
    strand_map = {s.name: s.id for s in strands}

    # -----------------------
    # selectbox
    # -----------------------
    racket_options = [UNSELECTED_OPTION] + list(racket_map.keys())
    vertical_options = [UNSELECTED_OPTION] + list(strand_map.keys())
    horizontal_options = [UNSELECTED_OPTION] + list(strand_map.keys())

    racket_name = st.selectbox(RACKET_LABEL, racket_options)
    vertical_name = st.selectbox(VERTICAL_LABEL, vertical_options)
    horizontal_name = st.selectbox(HORIZONTAL_LABEL, horizontal_options)

    racket_id = racket_map.get(racket_name)
    vertical_id = strand_map.get(vertical_name)
    horizontal_id = strand_map.get(horizontal_name)

    # 未選択ならNoneにする
    if racket_name == UNSELECTED_OPTION:
        racket_id = None
    if vertical_name == UNSELECTED_OPTION:
        vertical_id = None
    if horizontal_name == UNSELECTED_OPTION:
        horizontal_id = None

    set_date = st.date_input(SET_DATE_LABEL, value=None)
    break_date = st.date_input(BREAK_DATE_LABEL, value=None)
    tension = st.number_input(TENSION_LABEL, min_value=0, step=1)
    cost = st.number_input(COST_LABEL, min_value=0, step=100, value=0)
    memo = st.text_area(MEMO_LABEL)
    rating = st.slider(RATING_LABEL, 1, 10, 5)

    # -----------------------
    # 登録
    # -----------------------
    if st.button(REGISTER_BUTTON_LABEL):
        cost = None if cost == 0 else cost
        if racket_name == UNSELECTED_OPTION:
            st.error(RACKET_REQUIRED_ERROR)
            st.stop()
        if vertical_name == UNSELECTED_OPTION:
            st.error(VERTICAL_REQUIRED_ERROR)
            st.stop()
        if horizontal_name == UNSELECTED_OPTION:
            st.error(HORIZONTAL_REQUIRED_ERROR)
            st.stop()

        create_record(
            user_id=user.id,
            racket_id=racket_id,
            vertical_strand_id=vertical_id,
            horizontal_strand_id=horizontal_id,
            set_date=set_date,
            break_date=break_date,
            tension=int(tension) if tension else None,
            cost=cost,
            memo=memo if memo else None,
            rating=rating,
        )
        st.success(REGISTER_SUCCESS_MSG)