FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04

# Install AWS CLI
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
        curl \
        unzip \
    && curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm -rf awscliv2.zip aws \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
