FROM python:3.10-slim

RUN pip install mlflow psycopg2-binary

EXPOSE 5000

CMD ["mlflow", "server", \
     "--backend-store-uri", "sqlite:///mlflow/experiments.db", \
     "--default-artifact-root", "/mlflow/artifacts", \
     "--host", "0.0.0.0", \
     "--port", "5000"]
