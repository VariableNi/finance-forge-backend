from pydantic import BaseModel
from typing import Optional

# Что нужно передать с фронтенда, чтобы создать цель
class GoalCreate(BaseModel):
    title: str
    target_amount: float

# Что нужно передать, чтобы записать смену (транзакцию)
class TransactionCreate(BaseModel):
    amount: float
    goal_id: int
    comment: Optional[str] = None