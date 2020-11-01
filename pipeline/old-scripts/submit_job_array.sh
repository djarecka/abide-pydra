#!/bin/bash

base=/scratch/Thu/nlo
dataset=abide
site=CMU_b

# first go to data directory, grab all subjects,
# and assign to an array
pushd $base/$dataset/$site
subjs=($(ls sub-* -d))
popd

# take the length of the array
# this will be useful for indexing later
len=$(expr ${#subjs[@]} - 1) # len - 1

echo Spawning ${#subjs[@]} sub-jobs.

sbatch --array=0-$len fmriprep_single_subject.sh $base $dataset $site ${subjs[@]}
