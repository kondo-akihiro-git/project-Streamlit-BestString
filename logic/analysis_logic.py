from statistics import mean
from sqlmodel import Session, select
from model.model import Record, Strand
from model.init import engine

TENSION_BIN_WIDTH = 2


def _tension_bin_label(tension: int) -> str:
    start = (tension // TENSION_BIN_WIDTH) * TENSION_BIN_WIDTH
    end = start + TENSION_BIN_WIDTH - 1
    return f"{start}~{end}"


def _get_broken_records(user_id: int):
    """
    break_date が登録済みのレコードのみを対象に、
    縦ガットの名前・耐久日数などをまとめて返す（内部利用）
    """
    with Session(engine) as session:
        records = session.exec(
            select(Record).where(
                Record.user_id == user_id,
                Record.break_date.is_not(None),
                Record.set_date.is_not(None),
            )
        ).all()

        strands = session.exec(select(Strand)).all()
        strand_map = {s.id: s for s in strands}

        result = []
        for r in records:
            days = (r.break_date - r.set_date).days
            if days <= 0:
                continue
            strand = strand_map.get(r.vertical_strand_id)
            result.append({
                "strand_name": strand.name if strand else "未設定",
                "tension": r.tension,
                "days": days,
                "cost": r.cost,
                "rating": r.rating,
            })
        return result


def get_durability_overall(user_id: int):
    records = _get_broken_records(user_id)
    days_list = [r["days"] for r in records]
    if not days_list:
        return None
    return round(mean(days_list), 1)


def get_durability_by_strand(user_id: int):
    records = _get_broken_records(user_id)
    grouped: dict[str, list[int]] = {}
    for r in records:
        grouped.setdefault(r["strand_name"], []).append(r["days"])

    result = [
        {"strand_name": name, "avg_days": round(mean(days), 1), "count": len(days)}
        for name, days in grouped.items()
    ]
    result.sort(key=lambda x: x["avg_days"], reverse=True)
    return result


def get_durability_by_tension(user_id: int):
    records = _get_broken_records(user_id)
    grouped: dict[str, list[int]] = {}
    for r in records:
        if r["tension"] is None:
            continue
        label = _tension_bin_label(r["tension"])
        grouped.setdefault(label, []).append(r["days"])

    result = [
        {"tension_bin": label, "avg_days": round(mean(days), 1), "count": len(days)}
        for label, days in grouped.items()
    ]
    result.sort(key=lambda x: x["tension_bin"])
    return result


def get_cost_per_day_by_strand(user_id: int):
    records = _get_broken_records(user_id)
    grouped: dict[str, list[float]] = {}
    for r in records:
        if r["cost"] is None:
            continue
        grouped.setdefault(r["strand_name"], []).append(r["cost"] / r["days"])

    result = [
        {"strand_name": name, "avg_cost_per_day": round(mean(values), 1), "count": len(values)}
        for name, values in grouped.items()
    ]
    result.sort(key=lambda x: x["avg_cost_per_day"])
    return result


def get_cost_per_day_by_tension(user_id: int):
    records = _get_broken_records(user_id)
    grouped: dict[str, list[float]] = {}
    for r in records:
        if r["cost"] is None or r["tension"] is None:
            continue
        label = _tension_bin_label(r["tension"])
        grouped.setdefault(label, []).append(r["cost"] / r["days"])

    result = [
        {"tension_bin": label, "avg_cost_per_day": round(mean(values), 1), "count": len(values)}
        for label, values in grouped.items()
    ]
    result.sort(key=lambda x: x["tension_bin"])
    return result


def get_rating_by_strand(user_id: int):
    records = _get_broken_records(user_id)
    grouped: dict[str, list[int]] = {}
    for r in records:
        if r["rating"] is None:
            continue
        grouped.setdefault(r["strand_name"], []).append(r["rating"])

    result = [
        {"strand_name": name, "avg_rating": round(mean(values), 1), "count": len(values)}
        for name, values in grouped.items()
    ]
    result.sort(key=lambda x: x["avg_rating"], reverse=True)
    return result


def get_rating_by_tension(user_id: int):
    records = _get_broken_records(user_id)
    grouped: dict[str, list[int]] = {}
    for r in records:
        if r["rating"] is None or r["tension"] is None:
            continue
        label = _tension_bin_label(r["tension"])
        grouped.setdefault(label, []).append(r["rating"])

    result = [
        {"tension_bin": label, "avg_rating": round(mean(values), 1), "count": len(values)}
        for label, values in grouped.items()
    ]
    result.sort(key=lambda x: x["tension_bin"])
    return result