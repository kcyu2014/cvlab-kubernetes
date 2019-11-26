FROM nvcr.io/nvidia/pytorch:18.09-py3
MAINTAINER Firstname LastName<first.last@epfl.ch>


#####  Documentation #########
# From nvidia-pytorch repository, to maximize efficiency of V100 GPU.
# Miniconda is by-default installed and ready to use.
# **TODO** Make sure you change the following:
#   1. Adapt the conda installed packages for your own project.
#   2. Replace your <uid> and <username>


RUN "sh" "-c" "echo nameserver 8.8.8.8 >> /etc/resolv.conf"


## user: root permission
USER root

# Install some basic utilities
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    sudo \
    git \
    bzip2 \
    libx11-6 \
 && rm -rf /var/lib/apt/lists/*

# Install python packages via conda.
ENV CONDA_AUTO_UPDATE_CONDA=false
RUN conda install -y "conda>=4.4.11" && conda clean -ya
#################################################
# ADAPT this for your own project!!!
RUN conda install -y \
        h5py \
        matplotlib==3.0.0 \
        numpy==1.13.1 \
        pillow \
        graphviz \
        pytorch==0.4.1 \
        pyyaml \
        protobuf \
        scipy \
        torchvision=0.2.1 \
        tqdm==4.11.2 \
        && \
    conda clean -ya
RUN pip install \
        tensorboardX \
        visdom==0.1.1 \
        pydensecrf

#################################################



# Create user with UID=NB_UID and in the 'NB_GID' group
# and make sure these dirs are writable by the `NB_GID` group.
# Configure user and group

#################################################
# CHANGE THIS PART ACCORDINGLY !!!
ENV SHELL=/bin/bash \
    NB_USER=<your-name> \
    NB_UID=<your-uid> \
    NB_GROUP=CVLAB-unit \
    NB_GID=11166 \
    CONDA_DIR=<conda-path> remove this if you do not install conda
#################################################

ENV HOME=/home/$NB_USER

RUN groupadd $NB_GROUP -g $NB_GID
RUN useradd -m -s /bin/bash -N -u $NB_UID -g $NB_GID $NB_USER && \
    echo "${NB_USER}:${NB_USER}" | chpasswd && \
    usermod -aG sudo,adm,root ${NB_USER}
RUN chown -R ${NB_USER}:${NB_GROUP} ${HOME}
RUN chown $NB_USER:$NB_GID $CONDA_DIR

# The user gets passwordless sudo
RUN echo "${NB_USER}   ALL = NOPASSWD: ALL" > /etc/sudoers


## user: user permission
USER $NB_USER

