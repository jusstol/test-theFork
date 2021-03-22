# Start from a minimal Anaconda setup.
FROM continuumio/miniconda3:latest

# Add conda libraries path to PATH to make sure supervisord command works.
ENV PATH=/opt/conda/bin:$PATH

# Install regular Python librairies from pip and conda.
COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt
RUN conda install pandas -y --quiet
RUN conda install matplotlib -y --quiet
RUN conda install jupyter -y --quiet

# Start Jupyter in notebooks/ directory.
WORKDIR /dist/notebooks

# Run Supervisor in background then run Jupyter Notebooks.
CMD ["sh", "-c", "supervisord -c /dist/supervisor/supervisord.conf && jupyter notebook --ip='*' --port=8888 --no-browser --allow-root"]
