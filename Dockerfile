FROM python:3.5 as base

RUN apt-get update && \
    apt-get install -y apt-utils libssl-dev curl graphviz

FROM base AS builder
RUN curl -L -o /usr/bin/solc https://github.com/ethereum/solidity/releases/download/v0.4.21/solc-static-linux && \
    chmod +x /usr/bin/solc

RUN python3 -m venv /opt/relay
RUN /opt/relay/bin/pip install pip==18.0.0 setuptools==40.0.0

COPY ./constraints.txt /relay/constraints.txt
COPY ./requirements.txt /relay/requirements.txt

WORKDIR /relay

RUN /opt/relay/bin/pip install -c constraints.txt populus
RUN /opt/relay/bin/pip install -c constraints.txt -r requirements.txt

ENV THREADING_BACKEND gevent

COPY . /relay

RUN /opt/relay/bin/pip install -c constraints.txt .
RUN /opt/relay/bin/python -c 'import pkg_resources; print(pkg_resources.get_distribution("trustlines-relay").version)' >/opt/relay/VERSION

FROM base
RUN rm -rf /var/lib/apt/lists/*
ENV THREADING_BACKEND gevent
COPY --from=builder /opt/relay /opt/relay
RUN ln -s /opt/relay/bin/tl-relay /usr/local/bin/
WORKDIR /opt/relay

ENTRYPOINT ["tl-relay"]
