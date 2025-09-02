from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
sys.path.append(r"C:\Users\gech\Documents\Getachew_project\sales_data_warehouse")
from scripts.bronze.load_raw import load_raw_data
from scripts.silver.clean_transform import clean_transform_data
from scripts.gold.create_analytics import create_analytics

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 9, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'sales_etl_pipeline',
    default_args=default_args,
    description='ETL pipeline for Sales Data Warehouse',
    schedule_interval='@daily',
    catchup=False,
) as dag:
    load_raw = PythonOperator(
        task_id='load_raw',
        python_callable=load_raw_data,
        op_kwargs={'csv_path': r'C:\Users\gech\Documents\Getachew_project\sales_data_warehouse\datasets\sample_sales.csv'}
    )
    
    clean_transform = PythonOperator(
        task_id='clean_transform',
        python_callable=clean_transform_data,
    )
    
    create_analytics = PythonOperator(
        task_id='create_analytics',
        python_callable=create_analytics,
    )
    
    load_raw >> clean_transform >> create_analytics