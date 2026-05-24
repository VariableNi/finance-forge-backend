from datetime import datetime, timezone
from typing import List
from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Goal(Base):
    __tablename__ = "goals"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)  # Название цели
    target_amount: Mapped[float] = mapped_column(nullable=False)     # Сколько нужно накопить
    current_amount: Mapped[float] = mapped_column(default=0.0)       # Сколько уже есть

    # Связь с транзакциями: одна цель может иметь много ударов молота (доходов)
    transactions: Mapped[List["Transaction"]] = relationship(
        back_populates="goal", cascade="all, delete-orphan"
    )
    
class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    amount: Mapped[float] = mapped_column(nullable=False)            # Сумма (например, +13084)
    comment: Mapped[str] = mapped_column(String(255), nullable=True) # "Смена на Озоне 21.05"
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Внешний ключ: привязываем транзакцию к конкретной цели
    goal_id: Mapped[int] = mapped_column(ForeignKey("goals.id"), nullable=False)
    
    # Обратная связь к цели
    goal: Mapped["Goal"] = relationship(back_populates="transactions")