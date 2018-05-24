FROM nvidia/cuda:8.0-devel-ubuntu16.04

RUN apt-get update &&\
    apt-get install -y --no-install-recommends \
    git \   
    vim \	
    ca-certificates

WORKDIR /software/

RUN git clone https://github.com/ewanbarr/dedisp.git && \
    cd dedisp &&\
    git checkout arch61 &&\
    make -j 32 && \
    make install 

RUN git clone https://github.com/ewanbarr/peasoup.git && \
    cd peasoup && \
    make -j 32 && \
    make install 
   
RUN ldconfig /usr/local/lib


RUN apt-get install --no-install-recommends -y  python3 python3-dev python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip
RUN pip3 install pika

# Define working directory.
WORKDIR /pika_tests/
COPY consume.py .
COPY publish.py .
