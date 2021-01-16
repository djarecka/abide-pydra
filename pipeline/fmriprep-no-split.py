# abide pydra pipeline
# pydra v0.12
# run with /om2/user/nlo/miniconda/envs/pydra/bin/python -u fmriprep-loop-task.py
import pydra
from pydra.engine.task import SingularityTask
from pydra.engine.submitter import Submitter
from pydra.utils.messenger import AuditFlag, FileMessenger
import os

#####################################################################
DATASET = "abide"
SITE = "Yale"

BASE = "/om2/scratch/Thu/nlo"
DATADIR = f"/BASE/{DATASET}/{SITE}"
OUTDIR = f"/BASE/{DATASET}/{SITE}/derivatives"
CACHEDIR = f"{BASE}/pydra-cache/{DATASET}/{SITE}_ss"

FS_LICENSE = f"/BASE/.freesurfer_license.txt"
IMAGE = "/om4/group/gablab/data/singularity-images/fmriprep-20.2.0.sif"

if not os.path.exists(DATADIR.replace("/BASE", BASE)):
    os.makedirs(DATADIR.replace("/BASE", BASE))
if not os.path.exists(OUTDIR.replace("/BASE", BASE)):
    os.makedirs(OUTDIR.replace("/BASE", BASE))
if not os.path.exists(CACHEDIR.replace("/BASE", BASE)):
    os.makedirs(CACHEDIR.replace("/BASE", BASE))

# SUBJECT = ["sub-0050571","sub-0050572", "sub-0050573"]
BIDSDIR = f"{BASE}/{DATASET}/{SITE}"
SUBJECTS = [
    s
    for s in os.listdir(BIDSDIR)
    if (s.startswith("sub-") and os.path.isdir(os.path.join(BIDSDIR, s)))
]
#s= SUBJECTS[0] # testing

print(f"SUBJECT = {s}")
s="sub-0050628"
SUBWORKDIR = f"/BASE/fmriprep-workdir/{DATASET}/{SITE}/{s}"
if not os.path.exists(SUBWORKDIR.replace("/BASE", BASE)):
    os.makedirs(SUBWORKDIR.replace("/BASE", BASE))

CMD = f"fmriprep {DATADIR} {OUTDIR} \
participant --participant_label {s} --nprocs 2 \
--output-space fsaverage6 --use-aroma \
--skip-bids-validation --mem_mb 7500 \
--fs-license-file /BASE/freesurfer_license.txt \
--fs-subjects-dir {OUTDIR}/freesurfer \
--ignore slicetiming --cifti-output -w {SUBWORKDIR}".split()

print("Command:")
print(CMD)

#####################################################################
singu = SingularityTask(
    name="fmriprep",
    executable=CMD,
    image=IMAGE,
    cache_dir=CACHEDIR,
    bindings=[(BASE, "/BASE", "rw")],
    container_xargs=['--cleanenv'],
    audit_flags=AuditFlag.ALL,
    messenger=FileMessenger()
)

print()
print("SingularityTask inputs:")
print(singu.inputs)
print()
print("SingularityTask container_args:")
print(singu.container_args)
print()

SBATCH_ARGS = f"-J {SITE} -t 30:00:00 --mem=8GB --cpus-per-task=2 -p normal"
print(f"sbatch_args:{SBATCH_ARGS}")

with Submitter(plugin="slurm", sbatch_args=SBATCH_ARGS, max_jobs=400) as sub:
    singu(submitter=sub)
res = singu.result()
#res = singu(plugin="slurm", sbatch_args=SBATCH_ARGS, max_jobs=400)

print("Done running!")
print(res)
#print(f"res.output.stdout = {res.output.stdout}")
#print()
#print(f"res.output.return_code = {res.output.return_code}")
