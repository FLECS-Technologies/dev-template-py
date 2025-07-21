FROM --platform=linux/amd64 python:3.13-slim-bookworm AS builder

RUN apt-get update && \
    apt-get --yes --no-install-recommends install \
    git pipx && \
    pipx ensurepath && \
    pipx install hatch

WORKDIR /app

COPY ./src ./src
COPY ./pyproject.toml .
COPY ./README.md .
COPY ./LICENSE .

RUN /root/.local/bin/hatch build

FROM python:3.13-slim-bookworm AS installer

RUN apt-get update && \
    apt-get --yes --no-install-recommends install \
    pip g++ make && \
    apt-get --yes clean && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=bind,from=builder,source=/app/dist,target=/wheels pip install --no-cache-dir /wheels/*.whl --prefix /install


FROM python:3.13-slim-bookworm

COPY --from=installer /install/lib /usr/local/lib
COPY --from=installer /install/bin /usr/local/bin

ADD docker/fs/ /

ENTRYPOINT ["uvicorn", "dev_template_py.server:app", "--log-config=/config/log_conf.yaml", "--host", "0.0.0.0", "--port", "80"]
