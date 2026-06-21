from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import engine, get_db
import models
import schemas

# Создаем таблицы в SQLite
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Кузница Финансов API")

@app.get("/")
def read_root():
    return {"status": "success", "message": "Кузница работает, молот готов к бою!"}

# --- ПРОЕКТЫ ---

@app.post("/projects/")
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    new_project = models.Project(title=project.title, description=project.description)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return {"status": "Project created", "project_id": new_project.id, "title": new_project.title}

@app.get("/projects/")
def get_all_projects(db: Session = Depends(get_db)):
    return db.query(models.Project).all()

# --- ЦЕЛИ ---

@app.post("/goals/")
def create_goal(goal: schemas.GoalCreate, db: Session = Depends(get_db)):
    # Проверяем, существует ли проект, к которому привязываем цель
    project_exists = db.query(models.Project).filter(models.Project.id == goal.project_id).first()
    if not project_exists:
        raise HTTPException(status_code=404, detail="Проект с таким ID не найден!")

    # Создаем объект базы данных, вытаскивая данные из пришедшей схемы
    new_goal = models.Goal(
        title=goal.title,
        target_amount=goal.target_amount,
        project_id=goal.project_id  # <-- Дополнили аргумент при создании!
    )
    
    db.add(new_goal)
    db.commit()
    db.refresh(new_goal)
    
    return {"status": "Goal created", "goal_id": new_goal.id, "title": new_goal.title}

@app.get("/projects/{project_id}/goals/")
def get_goals_by_project(project_id: int, db: Session = Depends(get_db)):
    # 1. Запрашиваем цели из базы данных по project_id
    goals = db.query(models.Goal).filter(models.Goal.project_id == project_id).all()
    
    # 2. Явно пересобираем их в чистый список обычных Python-словарей.
    # Это избавит нас от капризов SQLAlchemy со связанными таблицами!
    result = []
    for goal in goals:
        result.append({
            "id": goal.id,
            "title": goal.title,
            "target_amount": goal.target_amount,
            "current_amount": goal.current_amount,
            "project_id": goal.project_id
        })
        
    return result