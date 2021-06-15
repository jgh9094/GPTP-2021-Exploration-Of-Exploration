# ======= USAGE =======
# Run interactively:
#   docker run -it --entrypoint bash <IMAGE TAG>
# To build image locally (instead of pulling from dockerhub)
#   docker build /PATH/TO/GPTP-2021/

# Pull a base image
FROM ubuntu:20.04

COPY . /opt/GPTP-2021

# To make installs not ask questions about timezones
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=America/New_York

########################################################
# install base dependencies, add repo -lgfortran GL/gl.h
# - all of the extra dev libraries + fortran(??!!) + cargo are for the R environment... :(
########################################################
RUN \
  apt-get update \
    && \
  apt-get install -y -qq --no-install-recommends \
    software-properties-common \
    curl \
    g++-10=10.2.0-5ubuntu1~20.04 \
    make=4.2.1-1.2 \
    cmake=3.16.3-1ubuntu1  \
    python3=3.8.2-0ubuntu2 \
    python3-pip \
    python3-virtualenv \
    git=1:2.25.1-1ubuntu3 \
    dirmngr \
    gpg-agent \
    pandoc \
    pandoc-citeproc \
    texlive-base \
    texlive-latex-extra \
    lmodern \
    && \
  echo "installed base dependencies"

# alias wire g++-10 up to g++ ln -s gcc-10 gcc &&
RUN cd /usr/bin/ && ln -s g++-10 g++ &&  cd /

########################################################
# install project python dependencies (listed in requirements.txt)
########################################################
RUN \
  pip3 install -r /opt/GPTP-2021/experiments/requirements.txt \
    && \
  pip3 install osfclient \
    && \
  echo "installed python dependencies"

########################################################
# download data, put into expected directories
########################################################


# ########################################################
# # install r + r dependencies
# # - https://rtask.thinkr.fr/installation-of-r-4-0-on-ubuntu-20-04-lts-and-tips-for-spatial-packages/
# ########################################################


########################################################
# download Empirical @ appropriate commit
########################################################
RUN \
  git clone https://github.com/amlalejini/Empirical.git /opt/Empirical && \
  cd /opt/Empirical && \
  git checkout b5c0d06d6fb765ac7fedd18e91ecbc2c054f51ff && \
  git submodule init && \
  git submodule update && \
  echo "download Empirical"

########################################################
# compile experiment code
########################################################
RUN \
  cd /opt/GPTP-2021 && \
  make native && \
  echo "Finished compiling experiments."

# ########################################################
# # build supplemental material (will run analyses)
# ########################################################
# RUN \
#   cd /opt/Tag-based-Genetic-Regulation-for-LinearGP && \
#   ./build_book.sh && \
#   echo "finished running data analyses and building the supplemental material"


WORKDIR /opt/GPTP-2021