# logic/record_logic.py
from datetime import date
from sqlmodel import Session, select
from model.model import Racket, Record, Strand
from model.init import engine


def get_rackets():
    with Session(engine) as session:
        return session.exec(select(Racket)).all()


def get_strands():
    with Session(engine) as session:
        return session.exec(select(Strand)).all()
    

def create_record(
    user_id: int,
    racket_id: int,
    vertical_strand_id: int,
    horizontal_strand_id: int,
    set_date: date | None,
    break_date: date | None,
    tension: int | None,
    cost: int | None,
    memo: str | None,
    rating: int | None,
):
    with Session(engine) as session:
        record = Record(
            user_id=user_id,
            racket_id=racket_id,
            vertical_strand_id=vertical_strand_id,
            horizontal_strand_id=horizontal_strand_id,
            set_date=set_date,
            break_date=break_date,
            tension=tension,
            cost=cost,
            memo=memo,
            rating=rating,
        )
        session.add(record)
        session.commit()

    print("レコード登録完了")