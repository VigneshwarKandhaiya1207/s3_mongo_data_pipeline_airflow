import json
import io
import pandas as pd
from airflow import DAG
from airflow.providers.mongo.hooks.mongo import MongoHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.decorators import task
from airflow.utils.dates import days_ago


with DAG(
    dag_id='s3_mongo_db_etl_pipeline',
    start_date=days_ago(1),
    schedule_interval='@daily',
    catchup=False
) as dag:
    
    @task(dag=dag)
    def read_from_s3_bucket():
        s3_hook=S3Hook(aws_conn_id="s3-mongo-airflow")
        bucket_name='s3-mongo-airflow'
        key='phisingData.csv'
        file_content = s3_hook.read_key(key, bucket_name)
        csv_data = io.StringIO(file_content)
        data = pd.read_csv(csv_data)
        data.reset_index(drop=True,inplace=True)
        records=list(json.loads(data.T.to_json()).values())

        return records

    @task(dag=dag)
    def insert_into_mongodb(records):
        DATABASE_NAME="networksecurity"
        mongo_hook=MongoHook(mongo_conn_id="mongodb-network-security")
        client=mongo_hook.get_conn()
        db=client.get_database(DATABASE_NAME)
        collection=db["phisingdata"]
        try:
            if collection.count_documents({}) > 0:
                print("Collection has records. Deleting existing records...")
                collection.delete_many({})
                print("Existing records deleted.")
            
            if records:
                collection.insert_many(records)
                print("Inserted {} records.".format(len(records)))
            else:
                print("No Data to insert into Mongo DB")
        except Exception as e:
            print(f"Error inserting into MongoDB: {e}")

s3_read=read_from_s3_bucket()
insert_into_mongodb(s3_read)



