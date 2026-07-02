import streamlit as st
from logic.top_logic import create_url
from word.top_word import (
    PAGE_TITLE,
    NAME_INPUT_LABEL,
    URL_GENERATE_INFO,
    NAME_REQUIRED_ERROR,
    URL_GENERATE_BUTTON_LABEL,
    URL_GENERATE_SUCCESS_MSG,
)


def show():
    st.title(PAGE_TITLE)
    name = st.text_input(NAME_INPUT_LABEL)
    st.write(URL_GENERATE_INFO)
    if st.button(URL_GENERATE_BUTTON_LABEL):
        if not name:
            st.error(NAME_REQUIRED_ERROR)
            return
        url = create_url(name)
        st.success(URL_GENERATE_SUCCESS_MSG)
        st.code(url)