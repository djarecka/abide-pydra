# abide pydra pipeline
# pydra v0.10
# run with /om2/user/nlo/miniconda/envs/pydra/bin/python abide-pipeline-testing.py
import pydra
from pydra.engine.task import SingularityTask, ShellCommandTask
from pydra.engine.submitter import Submitter
import os

#####################################################################

BASE = "/scratch/Thu/nlo"
DATADIR = "/BASE/abide/Yale"
OUTDIR = "/BASE/abide/Yale/derivatives"
CACHEDIR = "/scratch/Thu/nlo/pydra_cache_dir/20201102-Yale-50627"
WORKDIR = "/BASE/fmriprep_work_dir"

FS_LICENSE = "/home/nlo/.freesurfer_license.txt"
IMAGE = "/om4/group/gablab/data/singularity-images/fmriprep-v1.3.0p2.sif"

if not os.path.exists(DATADIR.replace("/BASE", BASE)):
    os.makedirs(DATADIR.replace("/BASE", BASE))
if not os.path.exists(OUTDIR.replace("/BASE", BASE)):
    os.makedirs(OUTDIR.replace("/BASE", BASE))

SUBJECT = "sub-0050627"


CMD = f"fmriprep {DATADIR} {OUTDIR} -w {WORKDIR} \
participant --participant_label {SUBJECT} --nthreads 1 \
--output-space fsaverage6 --use-aroma --ignore-aroma-denoising-errors \
--skip-bids-validation --mem_mb 9500 --fs-license-file {FS_LICENSE} \
--ignore slicetiming --cifti-output".split(
    " "
)


#####################################################################
singu = SingularityTask(
    name="fmriprep",
    executable=CMD,
    image=IMAGE,
    cache_dir=CACHEDIR,
    bindings=[(BASE, "/BASE", "rw")],
)


sbatch_args = "-J pydra-test -t 1-00:00:00 --mem=10GB --cpus-per-task=1"

with Submitter(plugin="slurm", sbatch_args=sbatch_args) as sub:
    singu(submitter=sub)
res = singu.result()


print("Done running!")
print(f"res.output.stdout = {res.output.stdout}")
print()
print(f"res.output.return_code = {res.output.return_code}")


# SAVE FMRIPREP OUTPUT
fmriprep_stdout = f'/home/nlo/scripts/abide-pydra/pipeline/{SUBJECT}.stdout'
fmriprep_stderr = f'/home/nlo/scripts/abide-pydra/pipeline/{SUBJECT}.stderr'

with open(fmriprep_stdout, 'w+') as f:
   f.write(str(res.output.stdout))

with open(fmriprep_stderr, 'w+') as f:
   f.write(str(res.output.stderr))
