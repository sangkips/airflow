import csv
import logging
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyDatasetOperator
from airflow.providers.google.cloud.hooks.gcs import GCSHook
from datetime import datetime, timedelta


default_args = {
    'owner': 'tc4a',
    'start_date': datetime(2023, 11, 13),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

def fetch_data_from_postgres(ds_nodash, data_interval_end):
    # Query data from postgresql database and save to csv
    # Upload data to Google bucket
    postgres_hook = PostgresHook(postgres_conn_id='postgres_localhost')
    conn = postgres_hook.get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM public.stream_zoomreports", (ds_nodash, data_interval_end))
    data = cursor.fetchall()

    # Assuming you want to save this data to a file before uploading to GCS
    file_path = f'dags/zoom_report_{ds_nodash}.csv'
    with open(file_path, 'w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerows(data)
    cursor.close()
    cursor.close()
    logging.info(f"Saved data to {file_path}")

def upload_data_to_gcs(ds_nodash):
    gcs_hook = GCSHook(gcp_conn_id='gcp_conn')
    bucket = 'tc4a-backet'
    file_path = f'dags/zoom_report_{ds_nodash}.csv'
    destination_blob_name = f'zoom/zoom_report_{ds_nodash}.csv'
    gcs_hook.upload(bucket, destination_blob_name,filename=file_path)

with DAG(
    'reports_data_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False

) as dag:
    fetch_data = PythonOperator(
        task_id='fetch_data_from_postgres',
        python_callable=fetch_data_from_postgres
    )
    
    upload_data = PythonOperator(
        task_id='upload_data_to_gcs',
        python_callable=upload_data_to_gcs,
        provide_context=True
    )
 
    load_data_to_bq = GCSToBigQueryOperator(
        task_id='load_data_to_bigquery',
        bucket='tc4a-backet',
        gcp_conn_id='gcp_conn',
        source_objects=['zoom/zoom_report_*.csv'],
        destination_project_dataset_table='visualization-app-404406.tc4a.zoom_reports',
        source_format='CSV',
        write_disposition='WRITE_TRUNCATE',
        skip_leading_rows=1,
    )

    fetch_data >> upload_data >> load_data_to_bq