from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

# ГЛОБАЛЬНЫЕ ПРОЕКТЫ (Кузница, Машина)
class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Один проект -> много целей
    goals: Mapped[List["Goal"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )

# ПОДЦЕЛИ ВНУТРИ ПРОЕКТОВ (Горн, Молот)
class Goal(Base):
    __tablename__ = "goals"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    target_amount: Mapped[float] = mapped_column(nullable=False)
    current_amount: Mapped[float] = mapped_column(default=0.0)

    # Привязка цели к проекту
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    project: Mapped["Project"] = relationship(back_populates="goals")

    # Одна цель -> много транзакций
    transactions: Mapped[List["Transaction"]] = relationship(
        back_populates="goal", cascade="all, delete-orphan"
    )

# ТРАНЗАКЦИИ (СМЕНЫ)
class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    amount: Mapped[float] = mapped_column(nullable=False)
    comment: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Привязка транзакции к цели
    goal_id: Mapped[int] = mapped_column(ForeignKey("goals.id"), nullable=False)
    goal: Mapped["Goal"] = relationship(back_populates="transactions")