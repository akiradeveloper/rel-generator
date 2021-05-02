FROM python:3.6

RUN mkdir /app
COPY requirements.txt /app

WORKDIR /app

RUN apt-get update \
  && apt-get install -y mecab \
  && apt-get install -y mecab-ipadic \
  && apt-get install -y libmecab-dev \
  && apt-get install -y mecab-ipadic-utf8 \
  && apt-get install -y swig \
  && apt-get install -y sudo

RUN pip install -r requirements.txt
RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git
RUN cd mecab-ipadic-neologd; ./bin/install-mecab-ipadic-neologd -n -a -y

COPY src/* /app