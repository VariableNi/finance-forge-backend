from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

# Импортируем наши настройки и модели
from database import engine, get_db
import models

# Магия SQLAlchemy: эта строчка смотрит на класс Base в models.py, 
# находит все таблицы (goals, transactions) и физически создает их в sqlite.
models.Base.metadata.create_all(bind=engine)

# Инициализируем само приложение FastAPI
app = FastAPI(title="Кузница Финансов API")

# Тестовый роут, просто проверить, что всё дышит
@app.get("/")
def read_root():
    return {"status": "success", "message": "Кузница работает, молот готов к бою!"}

@app.get("/goals/") 
def get_all_goals(db: Session = Depends(get_db)):
    goals = db.query(models.Goal).all()
    return goals

# --- НАШ ПЕРВЫЙ РАБОЧИЙ ЭНДПОИНТ ---
# Роут для создания новой финансовой цели (например, RTX 5060)
@app.post("/goals/")
def create_goal(title: str, target_amount: float, db: Session = Depends(get_db)):
    # 1. Создаем объект модели SQLAlchemy
    new_goal = models.Goal(title=title, target_amount=target_amount)
    
    # 2. Добавляем в сессию и сохраняем в базу
    db.add(new_goal)
    db.commit()
    
    # 3. Обновляем наш объект, чтобы база вернула сгенерированный id
    db.refresh(new_goal)
    
    return {"status": "Goal created", "goal_id": new_goal.id, "title": new_goal.title}