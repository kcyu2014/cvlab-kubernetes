#!/usr/bin/env bash

$username=`whoami`
$uid=`id -u`

python wrapper.py --f_path=$1 --runtime=0.001 --num_runs=10 --uid=`id -u` --username=`whoami`
kubectl create -f $1.job

# check job logs.
# kubectl logs job/kyu-pytorch-imagenet -c job-1