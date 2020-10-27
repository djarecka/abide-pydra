#!/bin/bash

#SBATCH -J abide_download
#SBATCH -t 4:00:00
#SBATCH --mem=64GB
#SBATCH --cpus-per-task=4
#SBATCH --partition=gablab

BASE='/scratch/Thu/$(whoami)'
if [ ! -d $BASE ]; then
  mkdir -p $BASE
fi

module add openmind/singularity/3.4.1
IMGPATH='/om4/group/gablab/data/singularity-images/datalad-v0.12.7.sif'


# run container
singularity exec -B $BASE:/base $IMGPATH datalad install -rg -J 4 ///abide/RawDataBIDS 
