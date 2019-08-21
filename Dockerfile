# To compile this with docker use:
# docker build --tag sigpyproc .
# Then to run it:
# docker run --rm -it sigpyproc
# To be able to access local disk on Mac OSX, you need to use Docker for Mac GUI
# and click on 'File sharing', then add your directory, e.g. /data/bl_pks
# Then to run it:
# docker run --rm -it -v /data/bl_pks:/mnt/data sigpyproc
# And if you want to access a port, you need to do a similar thing:
# docker run --rm -it -p 9876:9876 sigpyproc

# INSTALL BASE FROM KERN SUITE
FROM kernsuite/base:3
ARG DEBIAN_FRONTEND=noninteractive

ENV TERM xterm

######
# Do docker apt-installs
RUN docker-apt-install build-essential python-setuptools python-pip python-tk python3 python3-dev python3-pip
RUN docker-apt-install git vim
RUN docker-apt-install curl wget
RUN docker-apt-install make cmake
RUN docker-apt-install fftw3 fftw3-dev pkg-config
RUN docker-apt-install libomp-dev

#####
# Pip installation of python packages
# Q. Would using CONDA be better?
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install numpy matplotlib ipython

# Finally, install sigpyproc!
COPY . .
RUN python setup.py install

# Pika installation
#RUN apt-get install --no-install-recommends -y  python3 python3-dev python3-pip && \
#    rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip
RUN pip3 install pika

WORKDIR /pika_tests/

RUN git clone https://github.com/ewanbarr/pikaprocess.git && \
    cd pikaprocess && \
    git checkout peasoup && \
    cp pika_process.py ../


