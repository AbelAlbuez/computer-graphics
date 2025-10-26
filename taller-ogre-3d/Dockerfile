FROM --platform=linux/amd64 ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# Forzar arquitectura AMD64
RUN dpkg --add-architecture amd64 && \
    dpkg --print-architecture

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    python3:amd64 \
    python3-pip:amd64 \
    python3-dev:amd64 \
    python3-ogre-1.12:amd64 \
    libsdl2-dev:amd64 \
    libgl1-mesa-dev:amd64 \
    libglu1-mesa-dev:amd64 \
    libx11-dev:amd64 \
    x11-apps:amd64 \
    mesa-utils:amd64 \
    git \
    vim \
    nano \
    curl \
    wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instalar herramientas de Python
RUN pip3 install --no-cache-dir \
    pylint \
    black \
    autopep8

# Variables de entorno
ENV PYTHONPATH=/workspace \
    DISPLAY=host.docker.internal:0

WORKDIR /workspace

CMD ["/bin/bash"]