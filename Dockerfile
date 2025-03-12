FROM continuumio/miniconda3

WORKDIR /app
COPY environment.yml /app/environment.yml
COPY . /app
RUN conda env create -f environment.yml && conda clean --all -y
SHELL ["conda","run","-n","hand", "/bin/bash","-c"]
CMD ["conda","run","-n","hand","python","app.py"]