# Jupyter Notebook container for interactive analysis and visualization
# Lightweight container optimized for data analysis and reporting

FROM jupyter/scipy-notebook:python-3.10

LABEL maintainer="LLM Proteomics Research Team"
LABEL description="Jupyter notebook environment for proteomics LLM evaluation analysis"
LABEL version="1.0.0"

# Switch to root for installations
USER root

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    vim \
    graphviz \
    pandoc \
    texlive-xetex \
    texlive-fonts-recommended \
    texlive-plain-generic \
    libgraphviz-dev \
    && rm -rf /var/lib/apt/lists/*

# Switch back to jovyan user
USER ${NB_UID}

# Set working directory
WORKDIR /home/jovyan/work

# Copy requirements
COPY --chown=${NB_UID}:${NB_GID} requirements.txt requirements-dev.txt ./

# Install Python packages
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install -r requirements-dev.txt

# Install Jupyter extensions and tools
RUN pip install \
    jupyterlab==4.0.10 \
    jupyterlab-git==0.50.0 \
    jupyterlab-execute-time==3.1.0 \
    jupyterlab-code-formatter==2.2.1 \
    jupytext==1.16.1 \
    nbconvert==7.14.2 \
    nbformat==5.9.2 \
    ipywidgets==8.1.1 \
    widgetsnbextension==4.0.9 \
    voila==0.5.5

# Install proteomics-specific packages
RUN pip install \
    pyteomics==4.6.3 \
    biopython==1.83 \
    pronto==2.5.6 \
    goatools==1.4.0

# Install visualization packages
RUN pip install \
    plotly==5.18.0 \
    seaborn==0.13.1 \
    matplotlib==3.8.2 \
    altair==5.2.0 \
    bokeh==3.3.4 \
    holoviews==1.18.1 \
    panel==1.3.8 \
    ipympl==0.9.3

# Install statistical analysis packages
RUN pip install \
    scipy==1.11.4 \
    statsmodels==0.14.1 \
    scikit-learn==1.3.2 \
    pingouin==0.5.4 \
    lifelines==0.27.8

# Install ML packages
RUN pip install \
    scikit-learn==1.3.2 \
    xgboost==2.0.3 \
    lightgbm==4.3.0 \
    catboost==1.2.2 \
    imbalanced-learn==0.12.0

# Install NLP packages
RUN pip install \
    transformers==4.38.1 \
    sentence-transformers==2.5.0 \
    nltk==3.8.1 \
    spacy==3.7.4 \
    textblob==0.17.1

# Install data manipulation packages
RUN pip install \
    pandas==2.0.3 \
    polars==0.20.7 \
    pyarrow==15.0.0 \
    dask[complete]==2024.2.0

# Install utility packages
RUN pip install \
    tqdm==4.66.1 \
    joblib==1.3.2 \
    pyyaml==6.0.1 \
    python-dotenv==1.0.1 \
    jsonschema==4.21.1

# Install experiment tracking
RUN pip install \
    mlflow==2.10.2 \
    wandb==0.16.3

# Install code quality tools
RUN pip install \
    black==24.2.0 \
    ruff==0.2.2 \
    mypy==1.8.0 \
    nbqa==1.8.0

# Enable JupyterLab extensions
RUN jupyter labextension install @jupyter-widgets/jupyterlab-manager && \
    jupyter labextension install jupyterlab-plotly

# Configure Jupyter
RUN jupyter lab build

# Copy notebooks and data
COPY --chown=${NB_UID}:${NB_GID} notebooks/ ./notebooks/
COPY --chown=${NB_UID}:${NB_GID} data/ ./data/
COPY --chown=${NB_UID}:${NB_GID} configs/ ./configs/
COPY --chown=${NB_UID}:${NB_GID} src/ ./src/

# Create output directories
RUN mkdir -p ./outputs ./figures ./tables ./logs

# Set environment variables
ENV JUPYTER_ENABLE_LAB=yes \
    JUPYTER_TOKEN="" \
    JUPYTER_ALLOW_INSECURE_WRITES=true

# Expose Jupyter Lab port
EXPOSE 8888

# Configure startup
CMD ["start-notebook.sh", \
     "--NotebookApp.token=''", \
     "--NotebookApp.password=''", \
     "--NotebookApp.allow_origin='*'", \
     "--NotebookApp.base_url=/", \
     "--ip=0.0.0.0", \
     "--port=8888", \
     "--no-browser", \
     "--notebook-dir=/home/jovyan/work"]

# Example usage:
# Build:
#   docker build -f containers/notebooks_container.Dockerfile -t llm-proteomics-notebooks .
#
# Run:
#   docker run -p 8888:8888 -v $(pwd):/home/jovyan/work llm-proteomics-notebooks
#
# Run with GPU support (if needed):
#   docker run --gpus all -p 8888:8888 -v $(pwd):/home/jovyan/work llm-proteomics-notebooks
#
# Access:
#   Open browser to http://localhost:8888
