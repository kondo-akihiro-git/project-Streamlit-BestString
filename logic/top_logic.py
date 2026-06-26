# page/top_page.py
import uuid
from sqlmodel import Session, select
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
    print("URL発行完了")
    return url

def get_user(token: str):
    with Session(engine) as session:
        statement = select(User).where(User.token == token)
        user = session.exec(statement).first()
        print("ユーザー取得完了")
        return user