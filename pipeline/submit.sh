#!/bin/bash
#SBATCH -n 2
#SBATCH -t 4-00:00
#SBATCH --mem=4GB
#SBATCH -J MaxMun_c-submit 
#SBATCH -p gablab
#SBATCH -o %x-job%A.out

source /home/nlo/.bashrc
conda activate pydra
python -c "import pydra; print ('Pydra version: ', pydra.__version__)"

SCRIPT="/om2/scratch/Thu/nlo/scripts/pipeline/fmriprep-loop-task.py" # or specific function
CMD="python -u ${SCRIPT}"
#singularity exec /om4/group/gablab/data/singularity-images/fmriprep-20.2.0.sif bash -c "env | grep FREESU" 

echo $CMD
exec $CMD

