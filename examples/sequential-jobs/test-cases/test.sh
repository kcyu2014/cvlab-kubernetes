#!/usr/bin/env bash

PATH=$HOME/Dropbox/git/cvlab-kubernetes/examples/sequential-jobs:$PATH

# Test the basic begin.yaml. With a simple test.py script.
#. submit_jobs.sh old/begin.yaml 0.005 3

. submit_jobs.sh test-binbash.yaml 0.01 10