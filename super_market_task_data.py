from pathlib import Path

import airflow.utils.dates
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.sensors.python import PythonSensor
from airflow.sensors.bash import BashSensor

dag = DAG(
    dag_id='supermarket_data_checker_dag',
    start_date=airflow.utils.dates.days_ago(3),
    schedule_interval='0 16 * * *',
    default_args={'depends_on_past': True}
)

create_metrics = DummyOperator(task_id="create_metrics", dag=dag)


def _wait_for_supermarket(supermarket_id_):
    supermarket_path = Path("/data/" + supermarket_id_)
    data_files = supermarket_path.glob("data-*.csv")
    success_file = supermarket_path / "_SUCCESS"
    return data_files and success_file.exists()


for supermarket_id in range(1, 5):
    wait = PythonSensor(
        task_id=f"wait_for_supermarket_{supermarket_id}",
        python_callable=_wait_for_supermarket,
        op_kwargs={"supermarket_id_": f"supermarket{supermarket_id}"},
        timeout=600,
        dag=dag,
    )
    copy = DummyOperator(task_id=f"copy_to_raw_supermarket_{supermarket_id}", dag=dag)
    process = DummyOperator(task_id=f"process_supermarket_{supermarket_id}", dag=dag)
    wait >> copy >> process >> create_metrics
