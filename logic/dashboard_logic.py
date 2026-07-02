from datetime import date
from sqlmodel import Session, select
from model.model import Record, Racket, Strand
from model.init import engine


def get_records(user_id: int):

    with Session(engine) as session:

        records = session.exec(
            select(Record)
            .where(Record.user_id == user_id)
            .order_by(Record.created_at.desc())
        ).all()

        rackets = session.exec(select(Racket)).all()
        strands = session.exec(select(Strand)).all()

        racket_map = {r.id: r for r in rackets}
        strand_map = {s.id: s for s in strands}

        result = []

        for r in records:
            racket = racket_map.get(r.racket_id)
            vertical = strand_map.get(r.vertical_strand_id)
            horizontal = strand_map.get(r.horizontal_strand_id)
            result.append({
                "id": r.id,
                "racket_id": r.racket_id,
                "racket": racket.name if racket else "未設定",
                "vertical_strand_id": r.vertical_strand_id,
                "vertical_strand": vertical.name if vertical else "未設定",
                "vertical_image": vertical.image_url if vertical else None,
                "horizontal_strand_id": r.horizontal_strand_id,
                "horizontal_strand": horizontal.name if horizontal else "未設定",
                "set_date": r.set_date,
                "break_date": r.break_date,
                "tension": r.tension,
                "cost": r.cost,
                "memo": r.memo,
                "rating": r.rating,
                "created_at": r.created_at,
            })

        return result


# -----------------------
# 編集ダイアログ用
# -----------------------

def get_rackets():
    with Session(engine) as session:
        return session.exec(select(Racket)).all()


def get_strands():
    with Session(engine) as session:
        return session.exec(select(Strand)).all()


def get_record(record_id: int):
    """編集ダイアログの初期値表示用に1件取得"""
    with Session(engine) as session:
        record = session.get(Record, record_id)
        if not record:
            return None
        return {
            "id": record.id,
            "racket_id": record.racket_id,
            "vertical_strand_id": record.vertical_strand_id,
            "horizontal_strand_id": record.horizontal_strand_id,
            "set_date": record.set_date,
            "break_date": record.break_date,
            "tension": record.tension,
            "cost": record.cost,
            "memo": record.memo,
            "rating": record.rating,
        }


def update_record(
    record_id: int,
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
        record = session.get(Record, record_id)
        if not record:
            print("更新対象のレコードが見つかりません")
            return

        record.racket_id = racket_id
        record.vertical_strand_id = vertical_strand_id
        record.horizontal_strand_id = horizontal_strand_id
        record.set_date = set_date
        record.break_date = break_date
        record.tension = tension
        record.cost = cost
        record.memo = memo
        record.rating = rating

        session.add(record)
        session.commit()

    print("レコード更新完了")