FROM ubuntu:latest

RUN apt-get -y update && apt-get install -y\
    git \
    python
RUN git clone https://github.com/sasja/machikoro

CMD cd machikoro && git pull && python ./test.py
