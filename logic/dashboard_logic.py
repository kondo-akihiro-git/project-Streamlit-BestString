# logic/dashboard_logic.py
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

        # -----------------------
        # ここで「表示用に変換」
        # -----------------------
        result = []

        for r in records:
            racket = racket_map.get(r.racket_id)
            vertical = strand_map.get(r.vertical_strand_id)
            horizontal = strand_map.get(r.horizontal_strand_id)
            result.append({
                "id": r.id,
                "racket": racket.name if racket else "未設定",
                "vertical_strand": vertical.name if vertical else "未設定",
                "vertical_image": vertical.image_url if vertical else None,
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