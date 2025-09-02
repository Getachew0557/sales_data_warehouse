from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src import models

# Updated database connection URL with correct password
DATABASE_URL = "postgresql://postgres:root@localhost:5432/todo_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def archive_completed_tasks():
    db = SessionLocal()
    try:
        completed_tasks = db.query(models.TodoItem).filter(models.TodoItem.completed == True).all()
        for task in completed_tasks:
            archived_task = models.ArchivedTodoItem(
                title=task.title,
                description=task.description,
                completed=task.completed,
                created_at=task.created_at
            )
            db.add(archived_task)
            db.delete(task)
        db.commit()
    finally:
        db.close()

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 9, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'archive_todo_tasks',
    default_args=default_args,
    description='Archive completed to-do tasks daily',
    schedule_interval='@daily',
    catchup=False,
) as dag:
    archive_task = PythonOperator(
        task_id='archive_completed_tasks',
        python_callable=archive_completed_tasks,
    )