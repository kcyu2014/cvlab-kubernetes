#!/usr/bin/env bash

PATH=$HOME/Dropbox/git/cvlab-kubernetes/examples/sequential-jobs:$PATH

# Test the basic begin.yaml. With a simple test.py script.
#. submit_jobs.sh old/begin.yaml 0.005 3
if [ -z "$1" ]
then
#. submit_jobs.sh test-binbash.yaml 0.1 10
#. submit_jobs.sh test-binbash-2.yaml 0.1 10
#. submit_jobs.sh test-binbash-3.yaml 0.1 10
. submit_jobs.sh test-binbash-4.yaml 0.1 10
. submit_jobs.sh test-binbash-5.yaml 0.1 10
else
kubectl delete -f test-binbash.yaml.job
kubectl delete -f test-binbash-2.yaml.job
kubectl delete -f test-binbash-3.yaml.job
kubectl delete -f test-binbash-4.yaml.job
kubectl delete -f test-binbash-5.yaml.job

fi
