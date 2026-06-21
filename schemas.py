from pydantic import BaseModel
from typing import Optional

# Что нужно передать, чтобы создать проект
class ProjectCreate(BaseModel):
    title: str
    description: Optional[str] = None

# Что нужно передать с фронтенда, чтобы создать цель (ОБНОВЛЕНО)
class GoalCreate(BaseModel):
    title: str
    target_amount: float
    project_id: int  # <-- Тот самый обязательный аргумент, который ты хотел дополнить!

# Что нужно передать, чтобы записать смену (транзакцию)
class TransactionCreate(BaseModel):
    amount: float
    goal_id: int
    comment: Optional[str] = None