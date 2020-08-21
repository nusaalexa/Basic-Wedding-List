FROM python:3.8

ENV PYTHONUNBUFFERED 1
RUN mkdir /weddinglist
WORKDIR /weddinglist
COPY . /weddinglist
RUN pip install -r requirements.txt