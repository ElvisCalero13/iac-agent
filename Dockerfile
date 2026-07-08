FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY apps ./apps
COPY src ./src

RUN pip install --no-cache-dir -e .

RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    ca-certificates \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

ARG TERRAFORM_VERSION=1.9.8

RUN curl -fsSL \
    https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip \
    -o /tmp/terraform.zip \
    && unzip /tmp/terraform.zip -d /usr/local/bin \
    && chmod +x /usr/local/bin/terraform \
    && rm /tmp/terraform.zip

ENV TF_PLUGIN_CACHE_DIR=/terraform.d/plugin-cache

RUN mkdir -p /terraform.d/plugin-cache

RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    ca-certificates \
    gnupg \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    ca-certificates \
    gnupg \
    git \
    && mkdir -p -m 755 /etc/apt/keyrings \
    && curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg \
    | dd of=/etc/apt/keyrings/githubcli-archive-keyring.gpg \
    && chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
    > /etc/apt/sources.list.d/github-cli.list \
    && apt-get update \
    && apt-get install -y gh \
    && rm -rf /var/lib/apt/lists/*

RUN pip install boto3 PyGithub

ENTRYPOINT ["python", "-m", "apps.cli.main"]