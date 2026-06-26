# page/top_page.py
import uuid
import streamlit as st
from sqlmodel import Session
from model.model import User
from model.init import engine
from setting.setting import BASE_URL


def create_url():

    token = str(uuid.uuid4())
    with Session(engine) as session:
        user = User(token=token)
        session.add(user)
        session.commit()
        session.refresh(user)

    url = f"{BASE_URL}/?token={token}"

    return url