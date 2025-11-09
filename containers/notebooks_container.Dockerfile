FROM jupyter/scipy-notebook:latest

USER root

# Install additional packages
RUN pip install --no-cache-dir \
    openai \
    anthropic \
    google-generativeai

USER jovyan

WORKDIR /app/notebooks
