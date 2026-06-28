# MLOps-customer-churn-app
production-grade-mlops-v2/
├── .github/
│   └── workflows/
│       ├── ci.yml                     # Linting, unit tests, DVC validation
│       ├── cd-retrain.yml             # Triggered on push to main
│       ├── scheduled-retrain.yml      # Cron-based retraining (e.g., weekly)
│       └── deploy-serving.yml         # Builds and deploys FastAPI container
├── configs/
│   ├── validation.yaml                # Model metric thresholds (e.g., ROC-AUC > 0.8)
│   └── drift_thresholds.yaml          # Drift thresholds (e.g., data_drift_share < 0.2)
├── data/
│   ├── raw/                           # Raw data (DVC tracked)
│   └── processed/                     # Intermediate data (DVC tracked)
├── feature_repo/                      # Feast Feature Store Definitions
│   ├── feature_store.yaml             # Feast config (Offline: S3/Parquet, Online: Redis)
│   ├── entities.py                    # Entity definitions (e.g., customer_id)
│   ├── feature_views.py               # Feature transformations and SQL/Spark logic
│   └── data_sources.py                # Connections to raw data sources
├── metrics/                           # DVC tracked metrics (JSON)
├── models/                            # DVC tracked model artifacts
├── reports/                           # Drift detection HTML reports (DVC tracked)
├── scripts/                           # Utility scripts (e.g., DB setup, Feast materialization)
├── src/
│   ├── ingest.py                      # Ingest raw data and materialize to Feast Offline Store
│   ├── fetch_data.py                  # Fetch training dataset from Feast (point-in-time join)
│   ├── train.py                       # Model training & MLflow logging
│   ├── evaluate.py                    # Model evaluation & MLflow logging
│   ├── monitor_drift.py               # Evidently AI drift detection
│   └── gate.py                        # Validation gate (checks metrics + drift)
├── serving/                           # Model Serving Component
│   ├── app.py                         # FastAPI application logic
│   ├── mlflow_loader.py               # Helper to load model from MLflow
│   ├── Dockerfile                     # Container definition for FastAPI
│   └── requirements.txt               # Serving-specific dependencies
├── dvc.yaml                           # The DAG definition
├── dvc.lock                           # DAG lockfile
├── params.yaml                        # Hyperparameters and configurations
└── requirements.txt                   # Core pipeline dependencies





production-grade-mlops-v3/
├── .github/
│   └── workflows/
│       ├── ci.yml                     # Linting, unit tests
│       ├── cd-retrain.yml             # (Optional) Manual trigger for retrain
│       ├── deploy-airflow-dags.yml    # NEW: Syncs DAGs to Airflow server
│       └── deploy-serving.yml         # Builds and deploys FastAPI container
├── airflow/                           # NEW: Airflow specific configs
│   ├── docker-compose.yaml            # Local Airflow dev environment
│   ├── connections.json               # Airflow connections (DB, S3, Redis)
│   └── variables.json                 # Airflow variables
├── dags/                              # NEW: Airflow DAG definitions
│   ├── churn_training_dag.py          # Main training/retraining DAG
│   └── churn_drift_monitoring_dag.py  # Daily/Weekly drift monitoring DAG
├── configs/
│   ├── validation.yaml                
│   └── drift_thresholds.yaml          
├── data/                              # DVC tracked (Local dev only)
├── feature_repo/                      # Feast definitions
├── metrics/                           # DVC tracked
├── models/                            # DVC tracked
├── reports/                           # DVC tracked
├── scripts/                           
├── src/                               # Core logic (Now executed by Airflow tasks)
│   ├── ingest.py                      
│   ├── fetch_data.py                  
│   ├── train.py                       
│   ├── evaluate.py                    
│   ├── monitor_drift.py               
│   └── gate.py                        
├── serving/                           
├── dvc.yaml                           # DVC pipeline (Still used for local dev/caching)
├── dvc.lock                           
├── params.yaml                        
└── requirements.txt                   