# abide pydra pipeline
# pydra v0.10
# run with /om2/user/nlo/miniconda/envs/pydra/bin/python abide-pipeline-testing.py
import pydra
from pydra.engine.task import SingularityTask, DockerTask, ShellCommandTask
import os
#####################################################################
"""
original fmriprep script

WORKDIR='/workdir/fmriprep'
DATADIR='/mnt/data'
OUTDIR='/mnt/data/derivatives'
subject=${subjs[${SLURM_ARRAY_TASK_ID}]}
imgpath="/storage/gablab001/data/singularity-images/fmriprep-v1.3.0p2.sif"
FS_LICENSE='/home/nlo/.freesurfer_license.txt'

module add openmind/singularity/3.0.3

singularity exec -B $base:/mnt -B $scratch:/workdir -e $imgpath \
fmriprep $DATADIR $OUTDIR participant --participant_label $subject --nthreads 8 \
--output-space fsaverage6 --use-aroma --ignore-aroma-denoising-errors \
--skip-bids-validation --mem_mb 125000 --fs-license-file $FS_LICENSE \
--ignore slicetiming -w $WORKDIR --cifti-output
"""

BASE = "/scratch/Thu/nlo"
DATADIR = "/BASE/abide/Caltech"
OUTDIR = "/BASE/abide-processed/Caltech"
CACHEDIR = "/scratch/Thu/nlo/cache_dir"
WORKDIR = "/BASE/cache_dir"

FS_LICENSE = "/home/nlo/.freesurfer_license.txt"
IMAGE = "/om4/group/gablab/data/singularity-images/fmriprep-v1.3.0p2.sif"

if not os.path.exists(DATADIR.replace("/BASE", BASE)):
    os.makedirs(DATADIR.replace('/BASE', BASE))
if not os.path.exists(OUTDIR.replace("/BASE", BASE)):
    os.makedirs(OUTDIR.replace('/BASE', BASE))

SUBJECT = "sub-0051456"



CMD = f"fmriprep {DATADIR} {OUTDIR} -w {WORKDIR} \
participant --participant_label {SUBJECT} --nthreads 8 \
--output-space fsaverage6 --use-aroma --ignore-aroma-denoising-errors \
--skip-bids-validation --mem_mb 125000 --fs-license-file {FS_LICENSE} \
--ignore slicetiming  --cifti-output".split(' ') 


#####################################################################
singu = SingularityTask(name="fmriprep", 
                        executable=CMD, 
                        image=IMAGE, 
                        cache_dir=CACHEDIR,
                        bindings=[(BASE, "/BASE", "rw")],
                        )

print(f'singu.inputs.image = {singu.inputs.image}')
print()
print(f'singu.inputs.container = {singu.inputs.container}')
print()
print(f'singu.cmdline = {singu.cmdline}')
print()

res = singu()

print('Done running!')
print(f'res.output.stdout = {res.output.stdout}') 
print()
print(f'res.output.return_code = {res.output.return_code}')

