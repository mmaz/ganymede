FROM continuumio/miniconda3

# docker build -t callisto server/

# docker run --rm -p 9876:9876 -it callisto /bin/bash -c "python /callisto.py"


ENV DEBIAN_FRONTEND noninteractive
COPY callisto.py /callisto.py

RUN /opt/conda/bin/conda install flask -y --quiet