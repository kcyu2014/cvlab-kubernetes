#!/usr/bin/env bash

TEMPDIR=. # Change to later
#TEMPDIR=/Users/kyu/Dropbox/git/cvlab-kubernetes/examples/sequential-jobs/ # Change to later
LOGDIR=$TEMPDIR/logs
LOGFILE=$TEMPDIR/jobs.log

# TODO make this $1-3 meaningful and give message to other people.
#echo $TEMPDIR

FNAME=$1

USERID=0
#USERID=`id -u`
USER=`whoami`

python ${TEMPDIR}/wrapper.py \
    --f_path=$FNAME \
    --out_dir=LOGDIR \
    --username=$USER

# COPY the file to the new location.
NEWPATH=${LOGDIR}/${USER}-${USERID}-$(basename $FNAME).job
cp ${FNAME}.job $NEWPATH

kubectl delete -f ${NEWPATH}

DATE=$(date '+%d/%m/%Y %H:%M');
echo "$DATE : job (basename $FNAME) created, with {$RUN_TIME}h for {$NUM_RUN} number of runs." >> $LOGFILE ;

# check job logs.
# kubectl logs job/kyu-pytorch-imagenet -c job-1