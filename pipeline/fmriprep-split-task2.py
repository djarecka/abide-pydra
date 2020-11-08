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
CACHEDIR = "/scratch/Thu/nlo/pydra_cache_dir/Yale-50561-5"
WORKDIR = "/BASE/fmriprep_work_dir"

FS_LICENSE = "/home/nlo/.freesurfer_license.txt"
IMAGE = "/om4/group/gablab/data/singularity-images/fmriprep-v1.3.0p2.sif"

if not os.path.exists(DATADIR.replace("/BASE", BASE)):
    os.makedirs(DATADIR.replace("/BASE", BASE))
if not os.path.exists(OUTDIR.replace("/BASE", BASE)):
    os.makedirs(OUTDIR.replace("/BASE", BASE))

SUBJECT = ["sub-0050561", "sub-0050562", "sub-0050563", "sub-0050564", "sub-0050565"]
CMD_LIST = list()

for s in SUBJECT:
    CMD = f"fmriprep {DATADIR} {OUTDIR} -w {WORKDIR} \
    participant --participant_label {s} --nthreads 1 \
    --output-space fsaverage6 --use-aroma --ignore-aroma-denoising-errors \
    --skip-bids-validation --mem_mb 9500 --fs-license-file {FS_LICENSE} \
    --ignore slicetiming --cifti-output".split(" ")
    CMD_LIST.append(CMD)


#####################################################################
singu = SingularityTask(
    name="fmriprep",
    executable=CMD_LIST,
    image=IMAGE,
    cache_dir=CACHEDIR,
    bindings=[(BASE, "/BASE", "rw")],
).split("executable")

sbatch_args = "-J Yale-50561-5 -t 1-00:00:00 --mem=10GB --cpus-per-task=1"

with Submitter(plugin="slurm", sbatch_args=sbatch_args) as sub:
    singu(submitter=sub)
res = singu.result()


print("Done running!")
print(f"res.output.stdout = {res.output.stdout}")
print()
print(f"res.output.return_code = {res.output.return_code}")


# SAVE FMRIPREP OUTPUT
fmriprep_stdout = f"/home/nlo/scripts/abide-pydra/pipeline/{SUBJECT}.stdout"
fmriprep_stderr = f"/home/nlo/scripts/abide-pydra/pipeline/{SUBJECT}.stderr"

with open(fmriprep_stdout, "w+") as f:
    f.write(str(res.output.stdout))

with open(fmriprep_stderr, "w+") as f:
    f.write(str(res.output.stderr))
