import streamlit as st
import pandas as pd
import altair as alt
from streamlit_elements import elements, mui
from logic.analysis_logic import (
    get_durability_by_strand,
    get_durability_by_tension,
    get_cost_per_day_by_strand,
    get_cost_per_day_by_tension,
    get_rating_by_strand,
    get_rating_by_tension,
)
from word.state_word import USER_STATE

# おすすめボックス内のストリング名フォントサイズ（px）。ここを調整してください。
RECOMMEND_NAME_FONT_SIZE = 18
GRAPH_MARGIN_TOP = 3
BAR_COLOR = "#f8674f"

def _graph_margin():
    st.html(
        f"<div style='height:{GRAPH_MARGIN_TOP}px;'></div>"
    )

def _show_bar_section(title, data, index_key, index_label, value_key, value_label):
    _graph_margin()
    st.subheader(title)
    if not data:
        st.info("データがありません")
        return

    df = pd.DataFrame(data)
    df = df.rename(columns={index_key: index_label, value_key: value_label})

    with st.container(border=True):
        chart = (
            alt.Chart(df)
            .mark_bar(color=BAR_COLOR)
            .encode(
                x=alt.X(f"{value_label}:Q", title=value_label),
                y=alt.Y(
                    f"{index_label}:N",
                    title=None,
                    sort="-x",
                    axis=alt.Axis(labelAngle=0, labelLimit=300),
                ),
            )
        )
        st.altair_chart(chart, use_container_width=True)

        display_df = df[[index_label, value_label, "count"]].copy()
        display_df[value_label] = display_df[value_label].map(lambda x: f"{x:.1f}")
        display_df = display_df.rename(columns={"count": "件数"})
        st.table(display_df.set_index(index_label))


def _show_recommend_box(col, title, data, name_key, value_key, value_format, unit, element_key):
    with col:
        with st.container(border=True):
            st.write(title)
            if not data:
                st.info("データがありません")
                return
            top = data[0]
            with elements(element_key):
                mui.Typography(
                    top[name_key],
                    fontSize=RECOMMEND_NAME_FONT_SIZE,
                    fontWeight=600,
                )
            st.caption(f"{value_format.format(top[value_key])}{unit}")


def show():
    st.title("過去のガット分析")

    user = st.session_state.get(USER_STATE)
    if not user:
        st.error("ユーザー情報がありません")
        return

    durability_data = get_durability_by_strand(user.id)
    if not durability_data:
        st.info("まだ「切れた日」が登録された記録がないため、分析できるデータがありません")
        return

    cost_data = get_cost_per_day_by_strand(user.id)
    rating_data = get_rating_by_strand(user.id)

    col1, col2, col3 = st.columns(3)

    _show_recommend_box(
        col1, "耐久日数からのおすすめ", durability_data,
        "strand_name", "avg_days", "{:.1f}", "日",
        "recommend_durability"
    )
    _show_recommend_box(
        col2, "コストからのおすすめ", cost_data,
        "strand_name", "avg_cost_per_day", "{:.1f}", "円/日",
        "recommend_cost"
    )
    _show_recommend_box(
        col3, "打感からのおすすめ", rating_data,
        "strand_name", "avg_rating", "{:.1f}", "点",
        "recommend_rating"
    )

    _show_bar_section(
        "ストリングごとの耐久日数",
        durability_data,
        "strand_name", "ストリング名", "avg_days", "平均耐久日数",
    )

    _show_bar_section(
        "テンションごとの耐久日数",
        get_durability_by_tension(user.id),
        "tension_bin", "テンション帯", "avg_days", "平均耐久日数",
    )

    _show_bar_section(
        "ストリングごとのコスト",
        cost_data,
        "strand_name", "ストリング名", "avg_cost_per_day", "1日あたりコスト（円）",
    )

    _show_bar_section(
        "テンションごとのコスト",
        get_cost_per_day_by_tension(user.id),
        "tension_bin", "テンション帯", "avg_cost_per_day", "1日あたりコスト（円）",
    )

    _show_bar_section(
        "ストリングごとの打感",
        rating_data,
        "strand_name", "ストリング名", "avg_rating", "平均評価",
    )

    _show_bar_section(
        "テンションごとの打感",
        get_rating_by_tension(user.id),
        "tension_bin", "テンション帯", "avg_rating", "平均評価",
    )