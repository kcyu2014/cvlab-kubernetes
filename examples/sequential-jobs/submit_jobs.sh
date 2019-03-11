#!/usr/bin/env bash

$username=`whoami`
$uid=`id -u`

python wrapper.py --f_path=$1 --runtime=0.1 --num_runs=2 --uid=`id -u` --username=`whoami`
kubectl create -f $1.job

# check job logs.
# kubectl logs job/kyu-pytorch-imagenet -c job-1