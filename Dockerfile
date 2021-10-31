FROM alpine:3.4

COPY ./*.py /
COPY ./requirements.txt /requirements.txt
RUN echo "deb http://55.archive.ubuntu.com/ubuntu/ xenial main" >> /etc/apt/source.list
RUN echo "deb-src http://55.archive.ubuntu.com/ubuntu/ xenial main" >> /etc/apt/source.list
RUN echo "deb-src http://55.archive.ubuntu.com/ubuntu/ xenial main" >> /etc/apt/source.list
RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN apt-get upgrade -y iperf3
RUN pip3 install -r requirements.txt