FROM nvidia/cuda:8.0-cudnn6-devel-ubuntu16.04
MAINTAINER Kaicheng Yu <kaicheng.yu@epfl.ch>

RUN "sh" "-c" "echo nameserver 8.8.8.8 >> /etc/resolv.conf"

##########################
#####  Docmuemts #########
##########################

# Build a a light environment with the correct user access to cvlabdata3
# No root access originally, can sudo to get it
# Create to support k8s deployment and pod commmand
# Hope it can work!

############ user: root permission
USER root

# Pick up some dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        libfreetype6-dev \
        libjpeg-turbo8-dev \
        libpng12-dev \
        libzmq3-dev \
        pkg-config \
        python \
        python-tk \
        python-dev \
        psmisc \
        rsync \
        software-properties-common \
        sudo \
        unzip \
        wget \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -O https://bootstrap.pypa.io/get-pip.py && \
    python get-pip.py && \
    rm get-pip.py

# Install Matlab 9.1
# Must be run under VPN network
RUN curl -s http://install.iccluster.epfl.ch/scripts/soft/matlab/R2016b.sh >> /root/R2016b.sh && \
    chmod +x /root/R2016b.sh && \
    /root/R2016b.sh
ENV MATLAB_ROOT=/usr/local/MATLAB/R2016b
ENV PATH=$MATLAB_ROOT/bin:$PATH

ENV MATLAB_LIB=/usr/local/MATLAB/R2016b/sys/os/glnxa64/ \
    SYSTEM_LIB=/usr/lib/x86_64-linux-gnu/
#RUN mv $MATLAB_LIB/libstdc++.so.6.20 $MATLAB_LIB/bak-libstdc++.so.6.20 && \
#    mv $MATLAB_LIB/libstdc++.so.6 $MATLAB_LIB/bak-libstdc++.so.6 && \
#    ln -sf $SYSTEM_LIB/libstdc++.so.6.0.21 $MATLAB_LIB/libstdc++.so.6.0.21 && \
#    ln -sf $MATLAB_LIB/libstdc++.so.6.0.21 $MATLAB_LIB/libstdc++.so.6

WORKDIR $HOME/


# Configure user and group
ENV SHELL=/bin/bash \
    NB_USER=<your-name> \
    NB_UID=<your-uid> \
    NB_GROUP=CVLAB-unit \
    NB_GID=11166

ENV HOME=/home/$NB_USER


RUN groupadd $NB_GROUP -g $NB_GID
RUN useradd -m -s /bin/bash -N -u $NB_UID -g $NB_GID $NB_USER && \
    echo "${NB_USER}:${NB_USER}" | chpasswd && \
    usermod -aG sudo,adm,root ${NB_USER}
RUN chown -R ${NB_USER}:${NB_GROUP} ${HOME}

# The user gets passwordless sudo
RUN echo "${NB_USER}   ALL = NOPASSWD: ALL" > /etc/sudoers