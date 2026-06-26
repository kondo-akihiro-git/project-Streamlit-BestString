# model/init.py
import os
from sqlmodel import SQLModel, create_engine
from dotenv import load_dotenv
from model.model import *
from sqlmodel import Session

# =====================
# env
# =====================
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=False)


# =====================
# DB初期化
# =====================
def init_database():
    SQLModel.metadata.create_all(engine)


# =====================
# session取得
# =====================
def get_database_session():
    return Session(engine)


# =====================
# CLI起動用
# =====================
if __name__ == "__main__":
    init_database()
    print("DB作成完了")