# strand/yonex/insert.py
from sqlmodel import Session, select
# from model.init import engine
from model.init import get_database_session
from model.model import Strand
from strand.yonex.scraper import fetch_all

BRAND = "YONEX"

def insert_strands():
    data = fetch_all()
    with get_database_session() as session:
        for d in data:
            stmt = select(Strand).where(Strand.name == d["name"])
            exists = session.exec(stmt).first()
            if exists:
                continue
            strand = Strand(
                name=d["name"],
                brand=BRAND,
                image_url=d["image_url"],
            )
            session.add(strand)
        session.commit()


if __name__ == "__main__":
    insert_strands()
    print("insert完了")