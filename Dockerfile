FROM golang:latest

RUN apt-get update
RUN apt-get -y install git make time xdg-utils w3m
RUN git clone https://github.com/niklasfasching/go-org.git /tmp/go-org

WORKDIR /tmp/go-org

RUN time make setup
RUN time make preview
