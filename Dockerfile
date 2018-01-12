FROM ubuntu:16.04
#RUN apt-get install python3-pip && \
#    pip3 install --upgrade pip

RUN sed -i 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get -y upgrade && \
  #apt-get install -y build-essential && \
  #apt-get install -y software-properties-common && \
  #apt-get install -y  && \
    apt-get install --no-install-recommends -y  python3 python3-dev python3-pip && \
#    pip3 install -- upgrade pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip
RUN pip3 install pika
# Define working directory.
WORKDIR /tests
COPY consumer.py .
#RUN python3 consumer.py


