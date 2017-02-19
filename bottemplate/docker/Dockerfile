# sasja: first time docker, good enought for a poc

FROM ubuntu:latest

RUN apt-get -y update && apt-get install -y \
    git \
    python \
    python-pip

RUN pip install \
    requests \
    jsonschema

RUN git clone https://github.com/sasja/machikoro

CMD cd machikoro && git pull && python ./test.py
