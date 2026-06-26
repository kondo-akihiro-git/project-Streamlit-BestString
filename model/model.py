# model/model.py
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date 
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    token: str  
    name: str
    created_at: datetime = Field(default_factory=datetime.now)

class Racket(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    brand: str
    created_at: datetime = Field(default_factory=datetime.now)

class Strand(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    brand: str
    price: int
    created_at: datetime = Field(default_factory=datetime.now)

class Record(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    racket_id: int
    vertical_strand_id: int
    horizontal_strand_id: int
    set_date: date | None
    break_date: date | None
    tension: int | None
    cost: int | None
    memo: str | None
    rating: int | None       # 1〜10
    created_at: datetime = Field(default_factory=datetime.now)