# racket/yonex/nsert.py
from sqlmodel import Session, select
# from model.init import engine
from model.init import get_database_session
from model.model import Racket
from racket.yonex.scraper import fetch_all


BRAND = "YONEX"

def insert_rackets():
    data = fetch_all()
    with get_database_session() as session:
        for d in data:
            # -----------------------
            # 重複チェック
            # -----------------------
            stmt = select(Racket).where(Racket.name == d["name"])
            exists = session.exec(stmt).first()
            if exists:
                continue
            racket = Racket(
                name=d["name"],
                brand=BRAND,
            )
            session.add(racket)
        session.commit()

if __name__ == "__main__":
    insert_rackets()
    print("insert完了")