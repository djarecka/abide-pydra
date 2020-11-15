#!/bin/bash

# run fmriprep container for one subject
# this script takes in args
#   $1 - base directory
#   $2 - array of subjects

#SBATCH -J abide-fmriprep
#SBATCH -t 1-00:00:00
#SBATCH --mem=10GB
#SBATCH --cpus-per-task=1
#SBATCH -p normal

BASE=$1
DATASET=$2
SITE=$3

args=($@)
subjs=(${args[@]:3}) # drop initial arg (base)

# container args
DATADIR=/BASE/${DATASET}/${SITE}
OUTDIR=/BASE/${DATASET}/${SITE}/derivatives
WORKDIR='/BASE/fmriprep_work_dir'

SUBJECT=${subjs[${SLURM_ARRAY_TASK_ID}]}

module add openmind/singularity/3.0.3
IMGPATH="/storage/gablab001/data/singularity-images/fmriprep-v1.3.0p2.sif"
FS_LICENSE='/home/nlo/.freesurfer_license.txt'


echo Submitted job for: ${subject}

# run container
singularity exec -B $BASE:/BASE -e $IMGPATH \
fmriprep $DATADIR $OUTDIR participant --participant_label $SUBJECT \
 --nthreads 1 --output-space fsaverage6 \
--use-aroma --ignore-aroma-denoising-errors \
--skip-bids-validation --mem_mb 9500 --fs-license-file $FS_LICENSE \
--ignore slicetiming -w $WORKDIR --cifti-output 

