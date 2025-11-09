"""MLflow server configuration and startup."""
import mlflow
import os

def start_server():
    """Start MLflow tracking server."""
    backend_uri = os.getenv("MLFLOW_BACKEND_URI", "sqlite:///experiments.db")
    artifact_root = os.getenv("MLFLOW_ARTIFACT_ROOT", "./mlruns")
    
    mlflow.set_tracking_uri(backend_uri)
    print(f"MLflow server started: {backend_uri}")
    print(f"Artifacts: {artifact_root}")

if __name__ == "__main__":
    start_server()
