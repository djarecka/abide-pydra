#!/bin/bash
# delete fmirprep derivatives, pydra cache and fmriprep workdir

DATASET=abide2
SITE=ETHZ_1

DERIVATIVES_DIR=/om2/scratch/Thu/nlo/${DATASET}/${SITE}/derivatives/
CACHE_DIR=/om2/scratch/Thu/nlo/pydra-cache/${DATASET}/${SITE}
WORK_DIR=/om2/scratch/Thu/nlo/fmriprep-workdir/${DATASET}/${SITE}

cmd="rm -rf $DERIVATIVES_DIR $CACHE_DIR $WORK_DIR"
echo $cmd
exec $cmd
