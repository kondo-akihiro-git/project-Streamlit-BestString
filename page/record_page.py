# page/record_page.py
import streamlit as st
from datetime import date
from logic.record_logic import create_record, get_rackets, get_strands
from word.state_word import USER_STATE


def show():
    st.title("記録登録画面")

    user = st.session_state.get(USER_STATE)

    if not user:
        st.error("ユーザー情報がありません")
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
    racket_options = ["未選択"] + list(racket_map.keys())
    vertical_options = ["未選択"] + list(strand_map.keys())
    horizontal_options = ["未選択"] + list(strand_map.keys())

    racket_name = st.selectbox("ラケット", racket_options)
    vertical_name = st.selectbox("縦ストリング", vertical_options)
    horizontal_name = st.selectbox("横ストリング", horizontal_options)

    racket_id = racket_map.get(racket_name)
    vertical_id = strand_map.get(vertical_name)
    horizontal_id = strand_map.get(horizontal_name)

    # 未選択ならNoneにする
    if racket_name == "未選択":
        racket_id = None
    if vertical_name == "未選択":
        vertical_id = None
    if horizontal_name == "未選択":
        horizontal_id = None

    set_date = st.date_input("張った日", value=None)
    break_date = st.date_input("切れた日", value=None)
    tension = st.number_input("テンション", min_value=0, step=1)
    cost = st.number_input("金額", min_value=0, step=100, value=0)
    memo = st.text_area("打感メモ")
    rating = st.slider("評価", 1, 10, 5)

    # -----------------------
    # 登録
    # -----------------------
    if st.button("登録する"):
        cost = None if cost == 0 else cost
        if racket_name == "未選択":
            st.error("ラケットは必須です")
            st.stop()
        if vertical_name == "未選択":
            st.error("縦ストリングは必須です")
            st.stop()
        if horizontal_name == "未選択":
            st.error("横ストリングは必須です")
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
        st.success("登録完了")

