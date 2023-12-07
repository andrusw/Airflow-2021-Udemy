from airflow import DAG

from datetime import datetime, timedelta

default_ags ={
    "owner":"airflow",
    "email_on_failure":False,
    "email_on_retry": False,
    "email": "admin@localhost.com",
    "retries": 1,
    "retry_delay": timedelta(minutes=3) 
    }

with DAG(
    "forex_data_pipeline"
    ,default_ags=default_ags
    , start_date=datetime(2021,1,1)
    , schedule_interval="@daily"
    , catchup=False) as dag:

    is_forex_rates_available = HttpSensor(
        task_id="is_forex_rates_available",
        http_conn_id="forex_api",
        endpoint="marclamberti/f45f872dea4dfd3eaa015a4a1af4b39b",
        response_check=lambda response: "rates" in response.text,
        poke_interval=5,
        timeout=20
    )