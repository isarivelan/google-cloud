# Google Cloud ETL Project

## 📌 Project Overview
This project demonstrates an **ETL pipeline on Google Cloud** using **Apache Airflow (Cloud Composer)** and **Cloud Data Fusion**. The pipeline performs the following steps:

1. **Extract & Generate Data**: A Python script (`extract.py`) creates synthetic employee data using the Faker library and uploads it to a Google Cloud Storage (GCS) bucket.
2. **Trigger ETL Pipeline**: An Airflow DAG (`dag.py`) runs the extract script and then triggers a Cloud Data Fusion pipeline to process the uploaded data.

---

## 🏗 Architecture
- **Cloud Composer (Airflow)**: Orchestrates the workflow.
- **Google Cloud Storage (GCS)**: Stores the generated CSV file.
- **Cloud Data Fusion**: Executes the ETL pipeline.
- **Python & Faker**: Generates synthetic employee data.

Workflow:
```
Airflow DAG → BashOperator (extract.py) → GCS → CloudDataFusionStartPipelineOperator → Data Fusion ETL
```

---

## ✅ Prerequisites
- Google Cloud Project with **Cloud Composer**, **Cloud Data Fusion**, and **GCS** enabled.
- Python packages:
  - `faker`
  - `google-cloud-storage`
- A GCS bucket (e.g., `raw-emp-data`) for storing the CSV file.
- A Cloud Data Fusion instance and pipeline configured.

---

## ⚙️ Setup Instructions
1. **Create a GCS bucket**:
   ```bash
gsutil mb gs://raw-emp-data
   ```

2. **Upload DAG and script to Composer**:
   - Place `dag.py` under `/dags/` in your Composer environment.
   - Place `extract.py` under `/dags/scripts/`.

3. **Install dependencies in Composer**:
   - Add `faker` and `google-cloud-storage` to Composer PyPI packages.

4. **Update bucket name in `extract.py`**:
   ```python
bucket_name = 'raw-emp-data'  # Ensure no underscores
   ```

---

## 🔍 How the DAG Works (`dag.py`)
- Defines a DAG named `emp_data` scheduled to run daily.
- **Task 1**: `extract_data` runs `extract.py` via `BashOperator`.
- **Task 2**: `start_pipeline` triggers a Cloud Data Fusion pipeline using `CloudDataFusionStartPipelineOperator`.
- Dependency: `extract_data >> start_pipeline`.

---

## 🛠 How `extract.py` Works
- Generates 100 fake employee records with fields like name, email, job title, salary, and password.
- Saves data to `emp_data.csv`.
- Uploads the file to the specified GCS bucket using `google.cloud.storage`.

---

## 🚀 Deployment Steps
1. Upload files to Composer environment.
2. Verify DAG appears in Airflow UI.
3. Trigger the DAG manually or wait for the schedule.
4. Check GCS bucket for `emp_data.csv`.
5. Monitor Cloud Data Fusion pipeline execution.

---

## ✅ Best Practices
- Use **absolute paths** (e.g., `/tmp/emp_data.csv`) for file operations.
- Parameterize bucket names and file paths using Airflow Variables.
- Use **pendulum** for timezone-aware `start_date` in DAG.
- Avoid hardcoding credentials; use Composer’s service account.
- Implement retries and error handling for GCS uploads.

---

## 📂 File Structure
```
/dags/
   ├── dag.py
   └── scripts/
       └── extract.py
```

---

## 🔗 References
- [Cloud Composer Documentation](https://cloud.google.com/composer/docs)
- [Cloud Data Fusion Documentation](https://cloud.google.com/data-fusion/docs)
- [Airflow Operators](https://airflow.apache.org/docs/)
