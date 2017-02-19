FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    python \
    python-pip

RUN pip install \
    requests \
    jsonschema

COPY pythonmachibot.py .

CMD python pythonmachibot.py
