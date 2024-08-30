from datetime import timedelta, datetime
from airflow import DAG
from airflow.providers.google.cloud.transfers.postgres_to_gcs import PostgresToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCheckOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyTableOperator

# define default for DAGS
default_args = {
    'owner': 'tc4a',
    'start_date': datetime(2023, 11, 13),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# create dags instance
dag = DAG(
    'tc4a_data_visualization',
    default_args=default_args,
    description='An Airflow DAG for tc4a Postgres to BigQuery',
    schedule_interval=None,
    catchup=False
)

# Bigquery config parameters
BQ_CON_ID = "gcp_conn"
BQ_PROJECT = "visualization-app-404406"
BQ_DATASET = "tc4a"
BQ_TABLE1 = "attendance"
BQ_TABLE2 = "bq_courses"
BQ_TABLE3 = "bq_training"
BQ_TABLE4 = "bq_total_training_hours"
BQ_TABLE5 = "bq_organizations"
BQ_TABLE6 = "bq_professions"
BQ_TABLE7 = "bq_course_enrollments"
BQ_TABLE8 = "bq_accounts"
BQ_TABLE9 = "bq_zoomreports"
BQ_BUCKET = 'tc4a-backet'

# Postgres Config variables
PG_CON_ID = "postgres_localhost"
PG_SCHEMA = "public"

# Define tables from postgresql db
PG_TABLE1 = "lecture_watch_times"
PG_TABLE2 = "courses"
PG_TABLE3 = "lectures"
PG_TABLE4 = "organizations"
PG_TABLE5 = "professions"
PG_TABLE6 = "course_enrollments"
PG_TABLE7 = "accounts"
PG_TABLE8 = "stream_zoomreports"

# events, enrolments, attendance

# Define Json files stored in the GCP bucket
JSON_FILENAME1 = 'attendance_data_' + datetime.now().strftime('%Y-%m-%d') + '.json'
JSON_FILENAME2 = 'courses_data_' + datetime.now().strftime('%Y-%m-%d') + '.json'
JSON_FILENAME3 = 'training_data_' + datetime.now().strftime('%Y-%m-%d') + '.json'
JSON_FILENAME4 = 'organization_hours_' + datetime.now().strftime('%Y-%m-%d') + '.json'
JSON_FILENAME5 = 'organizations_' + datetime.now().strftime('%Y-%m-%d') + '.json'
JSON_FILENAME6 = 'profession_' + datetime.now().strftime('%Y-%m-%d') + '.json'
JSON_FILENAME7 = 'course_enrollments_' + datetime.now().strftime('%Y-%m-%d') + '.json'
JSON_FILENAME8 = 'accounts_' + datetime.now().strftime('%Y-%m-%d') + '.json'
JSON_FILENAME9 = 'zoom_reports_' + datetime.now().strftime('%Y-%m-%d') + '.json'

# Print project, dataset, and table information for debugging
print(f"Project: {BQ_PROJECT}")
print(f"Dataset: {BQ_DATASET}")
print(f"Table: {BQ_TABLE1}")

# Data Extraction
# Task to transfer data from postgres to Google cloud platform
postgres_zoom_reports_to_gcs = PostgresToGCSOperator(
    task_id='postgres_zoom_reports_to_gcs',
    sql=f'SELECT * FROM "{PG_SCHEMA}"."{PG_TABLE8}";',
    bucket=BQ_BUCKET,
    filename=JSON_FILENAME9,
    export_format='csv',
    postgres_conn_id=PG_CON_ID,
    field_delimiter=',',
    gzip=False,
    task_concurrency=1,
    gcp_conn_id=BQ_CON_ID,
    dag=dag,
)

# postgres_lecture_watch_times_to_gcs = PostgresToGCSOperator(
#     task_id='postgres_lecture_watch_times_to_gcs',
#     sql=f'SELECT * FROM "{PG_SCHEMA}"."{PG_TABLE1}";',
#     bucket=BQ_BUCKET,
#     filename=JSON_FILENAME1,
#     export_format='csv',
#     postgres_conn_id=PG_CON_ID,
#     field_delimiter=',',
#     gzip=False,
#     task_concurrency=1,
#     gcp_conn_id=BQ_CON_ID,
#     dag=dag,
# )
# postgres_organizations_to_gcs = PostgresToGCSOperator(
#     task_id='postgres_organizations_to_gcs',
#     sql=f'SELECT * FROM "{PG_SCHEMA}"."{PG_TABLE4}";',
#     bucket=BQ_BUCKET,
#     filename=JSON_FILENAME5,
#     export_format='csv',
#     postgres_conn_id=PG_CON_ID,
#     field_delimiter=',',
#     gzip=False,
#     task_concurrency=1,
#     gcp_conn_id=BQ_CON_ID,
#     dag=dag,
# )
# postgres_professions_to_gcs = PostgresToGCSOperator(
#     task_id='postgres_professions_to_gcs',
#     sql=f'SELECT * FROM "{PG_SCHEMA}"."{PG_TABLE5}";',
#     bucket=BQ_BUCKET,
#     filename=JSON_FILENAME6,
#     export_format='csv',
#     postgres_conn_id=PG_CON_ID,
#     field_delimiter=',',
#     gzip=False,
#     task_concurrency=1,
#     gcp_conn_id=BQ_CON_ID,
#     dag=dag,
# )
# postgres_course_enrollments_to_gcs = PostgresToGCSOperator(
#     task_id='postgres_course_enrollments_to_gcs',
#     sql=f'SELECT * FROM "{PG_SCHEMA}"."{PG_TABLE6}";',
#     bucket=BQ_BUCKET,
#     filename=JSON_FILENAME7,
#     export_format='csv',
#     postgres_conn_id=PG_CON_ID,
#     field_delimiter=',',
#     gzip=False,
#     task_concurrency=1,
#     gcp_conn_id=BQ_CON_ID,
#     dag=dag,
# )
# postgres_accounts_to_gcs = PostgresToGCSOperator(
#     task_id='postgres_accounts_to_gcs',
#     sql=f'SELECT * FROM "{PG_SCHEMA}"."{PG_TABLE7}";',
#     bucket=BQ_BUCKET,
#     filename=JSON_FILENAME8,
#     export_format='csv',
#     postgres_conn_id=PG_CON_ID,
#     field_delimiter=',',
#     gzip=False,
#     task_concurrency=1,
#     gcp_conn_id=BQ_CON_ID,
#     dag=dag,
# )
# postgres_count_organizations_hours_to_gcs = PostgresToGCSOperator(
#     task_id='count_organization_hours',
#     sql="""
#     SELECT 
#     SUM(
#         CASE
#             WHEN duration LIKE '%year%' THEN 365 * 24 -- assuming 1 year = 365 days
#             WHEN duration LIKE '%:%:%' AND POSITION(':' IN duration) > 0 THEN
#                 CASE
#                     WHEN SPLIT_PART(duration, ':', 1) <> '' AND SPLIT_PART(duration, ':', 2) <> '' AND SPLIT_PART(duration, ':', 3) <> '' THEN
#                         SPLIT_PART(duration, ':', 1)::INT +
#                         SPLIT_PART(duration, ':', 2)::INT / 60 +
#                         SPLIT_PART(duration, ':', 3)::INT / 3600
#                     ELSE 0
#                 END
#             WHEN duration LIKE '%:%' AND POSITION(':' IN duration) > 0 THEN
#                 CASE
#                     WHEN SPLIT_PART(duration, ':', 1) <> '' AND SPLIT_PART(duration, ':', 2) <> '' THEN
#                         SPLIT_PART(duration, ':', 1)::INT +
#                         SPLIT_PART(duration, ':', 2)::INT / 60
#                     ELSE 0
#                 END
#             WHEN duration LIKE '%min%' THEN
#                 CASE
#                     WHEN SPLIT_PART(duration, ' ', 1) <> '' THEN
#                         CAST(SPLIT_PART(duration, ' ', 1) AS INTEGER) / 60
#                     ELSE 0
#                 END
# 			WHEN duration LIKE '%hour%' THEN
#                 CASE
#                     WHEN POSITION(' ' IN duration) > 0 AND SPLIT_PART(duration, ' ', 1) <> '' THEN
#                         CAST(SPLIT_PART(duration, ' ', 1) AS INTEGER)
#                     ELSE 0
#                 END
#             WHEN duration LIKE '%Year%' THEN
#                 CASE
#                     WHEN POSITION(' ' IN duration) > 0 THEN
#                         CAST(SPLIT_PART(duration, ' ', 1) AS INTEGER) * 365 * 24 -- assuming 1 year = 365 days
#                     ELSE 0
#                 END
# 		 	WHEN duration LIKE '%minutes%' THEN
#                 CASE
#                     WHEN SPLIT_PART(duration, ' ', 3) <> '' THEN
#                         CAST(SPLIT_PART(duration, ' ', 3) AS INTEGER) / 60
#                     ELSE 0
#                 END
# 		 	WHEN duration LIKE '%Minute%' THEN
#                 CASE
#                     WHEN SPLIT_PART(duration, ' ', 3) <> '' THEN
#                         CAST(SPLIT_PART(duration, ' ', 3) AS INTEGER) / 60
#                     ELSE 0
#                 END
#             ELSE
#                 CASE
#                     WHEN duration <> '' THEN
#                         CAST(duration AS INTEGER) / 60 -- assuming plain numeric values are in minutes
#                     ELSE 0
#                 END
#         END
#     ) * COUNT(course_enrollments.completed_date)  AS total_duration_hours 
# FROM public.courses, public.course_enrollments
# WHERE organization_id=10;
#     """,
#     bucket=BQ_BUCKET,
#     filename=JSON_FILENAME4,
#     export_format='csv',
#     postgres_conn_id=PG_CON_ID,
#     field_delimiter=',',
#     gzip=False,
#     task_concurrency=1,
#     gcp_conn_id=BQ_CON_ID,
#     dag=dag,
# )

# postgres_course_to_gcs = PostgresToGCSOperator(
#     task_id='postgres_course_to_gcs',
#     # sql=f'SELECT * FROM "{PG_SCHEMA}"."{PG_TABLE2}";',
#     sql=f'SELECT id, created_at, updated_at, description, title, event_type, payment_type, language_id, organization_id, start_date_time, duration, specialization_id, cme, cpd, end_date_time, total_seats, remaining_seats, searchable, accessibility, country  FROM "{PG_SCHEMA}"."{PG_TABLE2}" ORDER BY id DESC;',
#     bucket=BQ_BUCKET,
#     filename=JSON_FILENAME2,
#     export_format='csv',
#     postgres_conn_id=PG_CON_ID,
#     field_delimiter=',',
#     gzip=False,
#     task_concurrency=1,
#     gcp_conn_id=BQ_CON_ID,
#     dag=dag,
# )

# postgres_lectures_to_gcs = PostgresToGCSOperator(
#     task_id='postgres_lectures_to_gcs',
#     # sql=f'SELECT * FROM "{PG_SCHEMA}"."{PG_TABLE3}";',
#     sql=f'SELECT * FROM "{PG_SCHEMA}"."{PG_TABLE3}" WHERE assessment_mandatory IS NOT NULL AND assessment_passing_score IS NOT NULL AND  attempt_limit IS NOT NULL ORDER BY id DESC;',
#     bucket=BQ_BUCKET,
#     filename=JSON_FILENAME3,
#     export_format='csv',
#     postgres_conn_id=PG_CON_ID,
#     field_delimiter=',',
#     gzip=False,
#     task_concurrency=1,
#     gcp_conn_id=BQ_CON_ID,
#     dag=dag,
# )

# # Loading data to BIGQUERY
# # Transfer data from GCS Bucket TO BigQuery
# bq_lecture_watch_times_load_csv = GCSToBigQueryOperator(
#     task_id="bq_lecture_watch_times_load_csv",
#     bucket=BQ_BUCKET,
#     source_objects=[JSON_FILENAME1],
#     destination_project_dataset_table=f"{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE1}",
#     schema_fields=[
#         {"name": "id", "type": "INTEGER", "mode": "REQUIRED"},
#         {"name": "watch_time", "type": "INTEGER", "mode": "NULLABLE"},
#         {"name": "account_id", "type": "INTEGER", "mode": "NULLABLE"},
#         {"name": "lecture_id", "type": "INTEGER", "mode": "NULLABLE"},
#         {"name": "created_at", "type": "TIMESTAMP", "mode": "NULLABLE"},
#         {"name": "updated_at", "type": "TIMESTAMP", "mode": "NULLABLE"},
#         {"name": "status", "type": "INTEGER", "mode": "NULLABLE"},
#         {"name": "completed_date", "type": "TIMESTAMP", "mode": "NULLABLE"},
#     ],
#     create_disposition='CREATE_IF_NEEDED',
#     write_disposition="WRITE_TRUNCATE",
#     gcp_conn_id=BQ_CON_ID,
#     dag=dag,
# )
# bq_organization_load_csv = GCSToBigQueryOperator(
#     task_id="bq_organization_load_csv",
#     bucket=BQ_BUCKET,
#     source_objects=[JSON_FILENAME5],
#     destination_project_dataset_table=f"{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE5}",
#     schema_fields=[
#         {"name": "id", "type": "INTEGER", "mode": "REQUIRED"},
#         {"name": "title", "type": "STRING", "mode": "NULLABLE"},
#         {"name": "created_at", "type": "TIMESTAMP", "mode": "NULLABLE"},
#         {"name": "updated_at", "type": "TIMESTAMP", "mode": "NULLABLE"},
#         {"name": "location", "type": "STRING", "mode": "NULLABLE"},
#         {"name": "description", "type": "STRING", "mode": "NULLABLE"},
#         {"name": "featured", "type": "BOOLEAN", "mode": "NULLABLE"},
#         {"name": "organization_code", "type": "STRING", "mode": "NULLABLE"},
#         {"name": "account_id", "type": "STRING", "mode": "NULLABLE"},
#         {"name": "special_organization", "type": "BOOLEAN", "mode": "NULLABLE"},
#     ],
#     create_disposition='CREATE_IF_NEEDED',
#     write_disposition="WRITE_TRUNCATE",
#     gcp_conn_id=BQ_CON_ID,
#     dag=dag,
# )

# bq_professions_load_csv = GCSToBigQueryOperator(
#     task_id="bq_professions_load_csv",
#     bucket=BQ_BUCKET,
#     source_objects=[JSON_FILENAME6],
#     destination_project_dataset_table=f"{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE6}",
#     schema_fields=[
#         {"name": "id", "type": "INTEGER", "mode": "REQUIRED"},
#         {"name": "name", "type": "STRING", "mode": "NULLABLE"},
#         {"name": "created_at", "type": "TIMESTAMP", "mode": "NULLABLE"},
#         {"name": "updated_at", "type": "TIMESTAMP", "mode": "NULLABLE"},
#     ],
#     create_disposition='CREATE_IF_NEEDED',
#     write_disposition="WRITE_TRUNCATE",
#     gcp_conn_id=BQ_CON_ID,
#     dag=dag,
# )

# bq_course_enrollments_load_csv = GCSToBigQueryOperator(
#     task_id="bq_course_enrollments_load_csv",
#     bucket=BQ_BUCKET,
#     source_objects=[JSON_FILENAME7],
#     destination_project_dataset_table=f"{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE7}",
#     schema_fields=[
#         {"name": "id", "type": "INTEGER", "mode": "REQUIRED"},
#         {"name": "account_id", "type": "INTEGER", "mode": "NULLABLE"},
#         {"name": "course_id", "type": "INTEGER", "mode": "NULLABLE"},
#         {"name": "enrollment_date", "type": "TIMESTAMP", "mode": "NULLABLE"},
#         {"name": "status", "type": "INTEGER", "mode": "REQUIRED"},
#         {"name": "enrolled", "type": "BOOLEAN", "mode": "NULLABLE"},
#         {"name": "course_watch_time", "type": "INTEGER", "mode": "NULLABLE"},
#         {"name": "feedback", "type": "BOOLEAN", "mode": "NULLABLE"},
#         {"name": "completed_date", "type": "TIMESTAMP", "mode": "NULLABLE"},
#     ],
#     create_disposition='CREATE_IF_NEEDED',
#     write_disposition="WRITE_TRUNCATE",
#     gcp_conn_id=BQ_CON_ID,
#     dag=dag,
# )
# bq_accounts_load_csv = GCSToBigQueryOperator(
#     task_id="bq_accounts_load_csv",
#     bucket=BQ_BUCKET,
#     source_objects=[JSON_FILENAME8],
#     destination_project_dataset_table=f"{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE8}",
#     schema_fields=[
#         {"name": "id", "type": "INTEGER", "mode": "REQUIRED"},
#         {"name": "first_name", "type": "STRING", "mode": "NULLABLE"},
#         {"name": "last_name", "type": "STRING", "mode": "NULLABLE"},
#         {"name": "email", "type": "STRING", "mode": "NULLABLE"},
#         {"name": "activated", "type": "BOOLEAN", "mode": "REQUIRED"},
#         {"name": "created_at", "type": "TIMESTAMP", "mode": "NULLABLE"},
#         {"name": "updated_at", "type": "TIMESTAMP", "mode": "NULLABLE"},
#         {"name": "gender", "type": "STRING", "mode": "NULLABLE"},
#         {"name": "profession_id", "type": "STRING", "mode": "NULLABLE"},
#         {"name": "country", "type": "STRING", "mode": "NULLABLE"},
#         {"name": "specialization_id", "type": "STRING", "mode": "NULLABLE"},
#     ],
#     create_disposition='CREATE_IF_NEEDED',
#     write_disposition="WRITE_TRUNCATE",
#     gcp_conn_id=BQ_CON_ID,
#     dag=dag,
# )

# bq_organization_training_hours_csv = GCSToBigQueryOperator(
#     task_id="bq_organization_training_hours_csv",
#     bucket=BQ_BUCKET,
#     source_objects=[JSON_FILENAME4],
#     destination_project_dataset_table=f"{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE4}",
#     schema_fields=[
#         {"name": "total_duration_hours ", "type": "INTEGER", "mode": "REQUIRED"},
#     ],
#     create_disposition='CREATE_IF_NEEDED',
#     write_disposition="WRITE_TRUNCATE",
#     gcp_conn_id=BQ_CON_ID,
#     dag=dag,
# )

# bq_course_load_csv = GCSToBigQueryOperator(
#     task_id="bq_course_load_csv",
#     bucket=BQ_BUCKET,
#     source_objects=[JSON_FILENAME2],
#     destination_project_dataset_table=f"{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE2}",
#     schema_fields=[
#         {"name": "id", "type": "INTEGER", "mode": "REQUIRED"},
#         {"name": "created_at", "type": "TIMESTAMP", "mode": "NULLABLE"},
#         {"name": "updated_at", "type": "TIMESTAMP", "mode": "NULLABLE"},
#         {"name": "description", "type": "STRING", "mode": "NULLABLE"},
#         {"name": "title", "type": "STRING", "mode": "NULLABLE"},
#         {"name": "event_type", "type": "INTEGER", "mode": "NULLABLE"},
#         {"name": "payment_type", "type": "INTEGER", "mode": "NULLABLE"},
#         {"name": "language_id", "type": "INTEGER", "mode": "NULLABLE"},
#         {"name": "organization_id", "type": "INTEGER", "mode": "NULLABLE"},
#         {"name": "start_date_time", "type": "TIMESTAMP", "mode": "NULLABLE"},
#         {"name": "duration", "type": "STRING", "mode": "NULLABLE"},
#         {"name": "specialization_id", "type": "INTEGER", "mode": "NULLABLE"},
#         {"name": "cme", "type": "INTEGER", "mode": "NULLABLE"},
#         {"name": "cpd", "type": "INTEGER", "mode": "NULLABLE"},
#         {"name": "end_date_time", "type": "TIMESTAMP", "mode": "NULLABLE"},
#         {"name": "total_seats", "type": "INTEGER", "mode": "NULLABLE"},
#         {"name": "remaining_seats", "type": "STRING", "mode": "NULLABLE"},
#         {"name": "searchable", "type": "BOOLEAN", "mode": "NULLABLE"},
#         {"name": "accessibility", "type": "INTEGER", "mode": "NULLABLE"},
#         {"name": "country", "type": "STRING", "mode": "NULLABLE"},
#     ],
#     create_disposition='CREATE_IF_NEEDED',
#     write_disposition="WRITE_TRUNCATE",
#     gcp_conn_id=BQ_CON_ID,
#     max_bad_records=100,
#     dag=dag,
# )

# bq_lectures_load_csv = GCSToBigQueryOperator(
#     task_id="bq_lectures_load_csv",
#     bucket=BQ_BUCKET,
#     source_objects=[JSON_FILENAME3],
#     destination_project_dataset_table=f"{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE3}",
#     schema_fields=[
#         {"name": "id", "type": "INTEGER", "mode": "REQUIRED"},
#         {"name": "title", "type": "STRING", "mode": "NULLABLE"},
#         {"name": "description", "type": "STRING", "mode": "NULLABLE"},
#         {"name": "course_id", "type": "INTEGER", "mode": "NULLABLE"},
#         {"name": "created_at", "type": "TIMESTAMP", "mode": "NULLABLE"},
#         {"name": "updated_at", "type": "TIMESTAMP", "mode": "NULLABLE"},
#         {"name": "duration", "type": "INTEGER", "mode": "NULLABLE"},
#         {"name": "assessment_mandatory", "type": "STRING", "mode": "NULLABLE"},
#         {"name": "assessment_passing_score", "type": "STRING", "mode": "NULLABLE"},
#         {"name": "attempt_limit", "type": "STRING", "mode": "NULLABLE"},
#         {"name": "access_status", "type": "BOOLEAN", "mode": "NULLABLE"},
#     ],
#     create_disposition='CREATE_IF_NEEDED',
#     write_disposition="WRITE_TRUNCATE",
#     gcp_conn_id=BQ_CON_ID,
#     max_bad_records=100,
#     dag=dag,
# )

bq_zoom_data_load_csv = GCSToBigQueryOperator(
    task_id="bq_zoom_data_load_csv",
    bucket=BQ_BUCKET,
    source_objects=[JSON_FILENAME9],
    destination_project_dataset_table=f"{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE9}",
    schema_fields=[
        {"name": "id", "type": "STRING", "mode": "REQUIRED"},
        {"name": "event_name", "type": "STRING", "mode": "REQUIRED"},
        {"name": "name", "type": "STRING", "mode": "NULLABLE"},
        {"name": "email", "type": "STRING", "mode": "NULLABLE"},
        {"name": "profession", "type": "STRING", "mode": "NULLABLE"},
        {"name": "country", "type": "STRING", "mode": "NULLABLE"},
        {"name": "county", "type": "STRING", "mode": "NULLABLE"},
        {"name": "duration", "type": "INTEGER", "mode": "NULLABLE"},
        {"name": "phone_number", "type": "STRING", "mode": "NULLABLE"},
        {"name": "board_number", "type": "STRING", "mode": "NULLABLE"},
        {"name": "medical_number", "type": "STRING", "mode": "NULLABLE"},
        {"name": "email_consent", "type": "BOOLEAN", "mode": "NULLABLE"},
        {"name": "specialization", "type": "STRING", "mode": "NULLABLE"},
        {"name": "gender", "type": "STRING", "mode": "NULLABLE"},
        {"name": "created_at", "type": "TIMESTAMP", "mode": "NULLABLE"},
        {"name": "updated_at", "type": "TIMESTAMP", "mode": "NULLABLE"},
    ],
    create_disposition='CREATE_IF_NEEDED',
    write_disposition="WRITE_TRUNCATE",
    gcp_conn_id=BQ_CON_ID,
    max_bad_records=100,
    dag=dag,
)

# Check that the data-table has dataset
# bq_lecture_watch_times_count = BigQueryCheckOperator(
#     task_id='bq_lecture_watch_times_count',
#     sql=f"SELECT COUNT(*) FROM `{BQ_DATASET}.{BQ_TABLE1}` WHERE `status` = 1 AND `watch_time` = 2427;",
#     use_legacy_sql=False,
#     gcp_conn_id=BQ_CON_ID,
#     dag=dag,
# )

# bq_course_count = BigQueryCheckOperator(
#     task_id='bq_course_count',
#     sql=f"SELECT COUNT(*) FROM `{BQ_DATASET}.{BQ_TABLE2}`;",
#     use_legacy_sql=False,
#     gcp_conn_id=BQ_CON_ID,
#     dag=dag,
# )

# bq_lectures_count = BigQueryCheckOperator(
#     task_id='bq_lectures_count',
#     sql=f"SELECT COUNT(*) FROM `{BQ_DATASET}.{BQ_TABLE3}`;",
#     use_legacy_sql=False,
#     gcp_conn_id=BQ_CON_ID,
#     dag=dag,
# )

# Transform >> to perform filtering, aggregation and joining

# postgres_lecture_watch_times_to_gcs >> bq_lecture_watch_times_load_csv >> bq_lecture_watch_times_count
# postgres_count_organizations_hours_to_gcs >> bq_organization_training_hours_csv
# postgres_course_to_gcs >> bq_course_load_csv >> bq_course_count
# postgres_lectures_to_gcs >> bq_lectures_load_csv >> bq_lectures_count
# postgres_organizations_to_gcs >> bq_organization_load_csv
# postgres_professions_to_gcs >> bq_professions_load_csv
# postgres_course_enrollments_to_gcs >> bq_course_enrollments_load_csv
# postgres_accounts_to_gcs >> bq_accounts_load_csv
postgres_zoom_reports_to_gcs >> bq_zoom_data_load_csv 