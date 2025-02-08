FROM postgres:latest

RUN apt-get update && \
  apt-get install -y git gcc make postgresql-server-dev-all && \
  rm -rf /var/lib/apt/lists/*

RUN git clone --branch v0.8.0 https://github.com/pgvector/pgvector.git

RUN cd pgvector && \
  make && \
  make install

RUN rm -rf pgvector
