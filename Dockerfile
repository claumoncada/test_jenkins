# Utilizar la imagen descargada al inicio
FROM jenkins/jenkins:latest

# Dependencias anaconda
USER root
RUN apt-get update && apt-get install -y \
    wget \
    bzip2 \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

# DInstalar anaconda
RUN wget https://repo.anaconda.com/archive/Anaconda3-2023.03-Linux-x86_64.sh -O /tmp/anaconda.sh \
    && bash /tmp/anaconda.sh -b -p /opt/anaconda \
    && rm /tmp/anaconda.sh

# Agregar al PATH y configurar
ENV PATH="/opt/anaconda/bin:$PATH"
USER jenkins