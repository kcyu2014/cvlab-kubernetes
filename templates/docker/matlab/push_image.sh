#!/bin/bash


docker build . -t $1
docker tag $1 ntxvm015.iccluster.epfl.ch/cvlab-k8s-master/$1
docker push ntxvm015.iccluster.epfl.ch/cvlab-k8s-master/$1
