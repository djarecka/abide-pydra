#!/bin/bash
#SBATCH -n 2
#SBATCH -t 1-00:00
#SBATCH --mem=8GB
#SBATCH -J err
#SBATCH -p gablab
#SBATCH -o %x-job%A.out

source /home/nlo/.bashrc
conda activate pydra

SCRIPT="/scratch/Thu/nlo/pytest_echo.py" # or specific function 

BASETEMP="/scratch/Thu/nlo/output/err/tmpdir"
PYTEST_OPTS="-vvs --durations=0"

CMD="pytest ${PYTEST_OPTS} --basetemp=${BASETEMP} ${SCRIPT}"
echo $CMD 
exec $CMD


