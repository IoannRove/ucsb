FROM python:3.8

WORKDIR /mnt/converter

RUN pip install --upgrade pip
COPY . .
RUN pip install .
