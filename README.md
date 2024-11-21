# s3_mongo_data_pipeline_airflow
Extract the data from S3 bucket and load into the Mongo DB using Airflow pipeline

### Project Overview: Airflow ETL Pipeline AWS S3 and MongoDB Integration

This project involves creating an ETL (Extract, Transform, Load) pipeline using Apache Airflow. The pipeline extracts data from AWS S3 bucket, transforms the data, and loads it into a MongoDB database. The entire workflow is orchestrated by Airflow, a platform that allows scheduling, monitoring, and managing workflows.

The project leverages Docker to run Airflow and MongoDB Atlas cluster, ensuring an isolated and reproducible environment. I also utilized Airflow hooks and operators to handle the ETL process efficiently.

## Steps to follow:

1. Create Virtual environment

````bash
conda create -p venv python==3.10 -y
conda activate ./venv
````

2. Initialize Astro to create the structure

````bash
astro init
````
3. Start the astro environment

````bash
astra dev start
````

4. Create connections (Admin -> Connections) from the Airflow UI for MongoDB and AWS S3 source connections.
5. Write your DAG under the dags folder (s3_mongo_etl_pipeline.py)
    * Extract the data from AWS S3 bucket
    * Insert the record into the `phisingdata` collection.
6. Restart astro environment.

````bash
astro dev restart
````
