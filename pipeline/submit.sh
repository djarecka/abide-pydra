#!/bin/bash
#SBATCH -n 2
#SBATCH -t 2-00:00
#SBATCH --mem=1GB
#SBATCH -J SDSU_1-submit
#SBATCH -p gablab
#SBATCH --no-requeue
#SBATCH -o %x-job%A.out
#SBATCH --mail-user=nlo@mit.edu
#SBATCH --mail-type=ALL,TIME_LIMIT

source /home/nlo/.bashrc
conda activate pydra
python -c "import pydra; print ('Pydra version: ', pydra.__version__)"

#SCRIPT="/om2/scratch/Thu/nlo/scripts/pipeline/fmriprep-no-split.py"
SCRIPT="/om2/scratch/Thu/nlo/scripts/pipeline/fmriprep-loop-task.py" # or specific function
CMD="python -u ${SCRIPT}"
#singularity exec /om4/group/gablab/data/singularity-images/fmriprep-20.2.0.sif bash -c "env | grep FREESU" 

echo $CMD
exec $CMD

