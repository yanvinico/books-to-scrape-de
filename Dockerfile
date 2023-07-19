FROM python:3

WORKDIR /src

COPY . .

RUN apt-get update && \
    apt-get install -y wget && \
    wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    echo "export PATH=/opt/conda/bin:$PATH" >> ~/.bashrc && \
    /opt/conda/bin/conda init bash

# Configuração do Conda
SHELL ["/bin/bash", "--login", "-c"]
RUN conda init bash
RUN echo "source activate books" >> ~/.bashrc

RUN conda env create -f environment.yml


CMD ["python", "src/ingestion.py"] 