#!/bin/bash
# delete fmirprep derivatives, pydra cache and fmriprep workdir

DATASET=abide
SITE=KKI
SUB=sub-0050774

FMRIPREP_DIR=/om2/scratch/Thu/nlo/${DATASET}/${SITE}/derivatives/fmriprep/${SUB}*
FREESURFER_DIR=/om2/scratch/Thu/nlo/${DATASET}/${SITE}/derivatives/freesurfer/${SUB}
CACHE_DIR=/om2/scratch/Thu/nlo/pydra-cache/${DATASET}/${SITE}/${SUB}
WORK_DIR=/om2/scratch/Thu/nlo/fmriprep-workdir/${DATASET}/${SITE}/${SUB}

cmd="rm -rf $FMRIPREP_DIR $FREESURFER_DIR $CACHE_DIR $WORK_DIR"
echo $cmd
exec $cmd
