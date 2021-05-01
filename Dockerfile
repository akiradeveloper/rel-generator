FROM python:3.6

RUN mkdir /app
COPY requirements.txt /app

WORKDIR /app
RUN pip install -r requirements.txt

RUN apt-get update \
  && apt-get install -y mecab \
  && apt-get install -y mecab-ipadic \
  && apt-get install -y libmecab-dev \
  && apt-get install -y mecab-ipadic-utf8 \
  && apt-get install -y swig

COPY src/* /app