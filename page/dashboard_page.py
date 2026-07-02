import streamlit as st
from streamlit_elements import elements, mui

from logic.dashboard_logic import (
    get_records,
    get_rackets,
    get_strands,
    get_record,
    update_record,
)
from word.state_word import USER_STATE, EDIT_RECORD_STATE, UPDATE_SUCCESS_STATE
from word.dashboard_word import (
    PAGE_TITLE,
    NO_USER_ERROR,
    NO_RECORD_INFO,
    UPDATE_SUCCESS_MSG,
    DIALOG_TITLE,
    RECORD_NOT_FOUND_ERROR,
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
    UPDATE_BUTTON_LABEL,
    CANCEL_BUTTON_LABEL,
    EDIT_BUTTON_LABEL,
    RACKET_REQUIRED_ERROR,
    VERTICAL_REQUIRED_ERROR,
    HORIZONTAL_REQUIRED_ERROR,
    SAME_STRAND_TEXT,
    VERTICAL_STRAND_TEXT,
    HORIZONTAL_STRAND_TEXT,
    RACKET_TEXT,
    SET_DATE_TEXT,
)
from style.dashboard_style import (
    TYPOGRAPHY_VARIANT,
    CARD_ELEVATION,
    CONTAINER_BORDER,
    CONTAINER_GAP,
    BROKEN_CARD_SX,
    NORMAL_CARD_SX,
    CARD_CONTENT_SX,
    TITLE_BOX_SX,
    IMAGE_BOX_SX_TEMPLATE,
)


@st.dialog(DIALOG_TITLE)
def edit_dialog(record_id: int):
    record = get_record(record_id)
    if not record:
        st.error(RECORD_NOT_FOUND_ERROR)
        return

    rackets = get_rackets()
    strands = get_strands()
    racket_map = {r.name: r.id for r in rackets}
    strand_map = {s.name: s.id for s in strands}
    racket_options = [UNSELECTED_OPTION] + list(racket_map.keys())
    vertical_options = [UNSELECTED_OPTION] + list(strand_map.keys())
    horizontal_options = [UNSELECTED_OPTION] + list(strand_map.keys())

    def _index_of(options, id_map, current_id):
        name = next((n for n, i in id_map.items() if i == current_id), UNSELECTED_OPTION)
        return options.index(name)

    racket_name = st.selectbox(
        RACKET_LABEL, racket_options,
        index=_index_of(racket_options, racket_map, record["racket_id"]),
    )
    vertical_name = st.selectbox(
        VERTICAL_LABEL, vertical_options,
        index=_index_of(vertical_options, strand_map, record["vertical_strand_id"]),
    )
    horizontal_name = st.selectbox(
        HORIZONTAL_LABEL, horizontal_options,
        index=_index_of(horizontal_options, strand_map, record["horizontal_strand_id"]),
    )
    racket_id = racket_map.get(racket_name)
    vertical_id = strand_map.get(vertical_name)
    horizontal_id = strand_map.get(horizontal_name)
    set_date = st.date_input(SET_DATE_LABEL, value=record["set_date"])
    break_date = st.date_input(BREAK_DATE_LABEL, value=record["break_date"])
    tension = st.number_input(TENSION_LABEL, min_value=0, step=1, value=record["tension"] or 0)
    cost = st.number_input(COST_LABEL, min_value=0, step=100, value=record["cost"] or 0)
    memo = st.text_area(MEMO_LABEL, value=record["memo"] or "")
    rating = st.slider(RATING_LABEL, 1, 10, value=record["rating"] or 5)

    col1, col2 = st.columns(2)
    with col1:
        if st.button(UPDATE_BUTTON_LABEL, use_container_width=True):
            if racket_name == UNSELECTED_OPTION:
                st.error(RACKET_REQUIRED_ERROR)
                st.stop()
            if vertical_name == UNSELECTED_OPTION:
                st.error(VERTICAL_REQUIRED_ERROR)
                st.stop()
            if horizontal_name == UNSELECTED_OPTION:
                st.error(HORIZONTAL_REQUIRED_ERROR)
                st.stop()

            update_record(
                record_id=record_id,
                racket_id=racket_id,
                vertical_strand_id=vertical_id,
                horizontal_strand_id=horizontal_id,
                set_date=set_date,
                break_date=break_date,
                tension=int(tension) if tension else None,
                cost=None if cost == 0 else cost,
                memo=memo if memo else None,
                rating=rating,
            )
            st.session_state.pop(EDIT_RECORD_STATE, None)
            st.session_state[UPDATE_SUCCESS_STATE] = True
            st.rerun()
    with col2:
        if st.button(CANCEL_BUTTON_LABEL, use_container_width=True):
            st.session_state.pop(EDIT_RECORD_STATE, None)
            st.rerun()


def show():
    user = st.session_state.get(USER_STATE)
    st.title(PAGE_TITLE)
    if not user:
        st.error(NO_USER_ERROR)
        return
    if st.session_state.pop(UPDATE_SUCCESS_STATE, False):
        st.success(UPDATE_SUCCESS_MSG)
    records = get_records(user.id)
    if not records:
        st.info(NO_RECORD_INFO)
        return
    if st.session_state.get(EDIT_RECORD_STATE):
        edit_dialog(st.session_state[EDIT_RECORD_STATE])

    # -----------------------
    # ガット表示
    # -----------------------
    cols = st.columns(2)
    for i, r in enumerate(records):
        col = cols[i % 2]
        with col:
            is_broken = bool(r["break_date"])
            card_sx = BROKEN_CARD_SX if is_broken else NORMAL_CARD_SX
            with st.container(border=CONTAINER_BORDER, gap=CONTAINER_GAP):
                with elements(f"dashboard_card_{r['id']}"):
                    with mui.Card(sx=card_sx, elevation=CARD_ELEVATION):
                        with mui.CardContent(sx=CARD_CONTENT_SX):
                            with mui.Box(sx=TITLE_BOX_SX):
                                vertical = r["vertical_strand"]
                                horizontal = r["horizontal_strand"]
                                if vertical == horizontal:
                                    mui.Typography(
                                        SAME_STRAND_TEXT.format(vertical=vertical),
                                        variant=TYPOGRAPHY_VARIANT,
                                    )
                                else:
                                    mui.Typography(
                                        VERTICAL_STRAND_TEXT.format(vertical=vertical),
                                        variant=TYPOGRAPHY_VARIANT,
                                    )
                                    mui.Typography(
                                        HORIZONTAL_STRAND_TEXT.format(horizontal=horizontal),
                                        variant=TYPOGRAPHY_VARIANT,
                                    )
                            image_box_sx = dict(IMAGE_BOX_SX_TEMPLATE)
                            image_box_sx["backgroundImage"] = image_box_sx["backgroundImage"].format(
                                image_url=r["vertical_image"]
                            )
                            with mui.Box(sx=image_box_sx):
                                pass
                            mui.Divider()
                            mui.Typography(
                                RACKET_TEXT.format(racket=r["racket"]),
                                variant=TYPOGRAPHY_VARIANT,
                            )
                            mui.Typography(
                                SET_DATE_TEXT.format(set_date=r["set_date"]),
                                variant=TYPOGRAPHY_VARIANT,
                            )

                if st.button(
                    EDIT_BUTTON_LABEL,
                    key=f"edit_btn_{r['id']}",
                    use_container_width=True,
                ):
                    st.session_state[EDIT_RECORD_STATE] = r["id"]
                    st.rerun()