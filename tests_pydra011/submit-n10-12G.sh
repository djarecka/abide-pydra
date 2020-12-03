#!/bin/bash
#SBATCH -n 10
#SBATCH -t 1-00:00
#SBATCH --mem=12GB
#SBATCH -J fmriprep-n10-12G
#SBATCH -p gablab
#SBATCH -o %x-job%A.out

source /home/nlo/.bashrc
conda activate pydra
python -c "import pydra; print ('Pydra version: ', pydra.__version__)"

SCRIPT="/om2/scratch/Thu/nlo/pytest_echo.py" # or specific function 

BASETEMP="/om2/scratch/Thu/nlo/tmpdir/fmriprep/n10-12G"
PYTEST_OPTS="-vvs --durations=0"

CMD="pytest ${PYTEST_OPTS} --basetemp=${BASETEMP} ${SCRIPT}"
echo $CMD 
exec $CMD


