# abide pydra pipeline
# pydra v0.12
# run with /om2/user/nlo/miniconda/envs/pydra/bin/python -u fmriprep-loop-task.py
import pydra
from pydra.engine.task import SingularityTask
from pydra.engine.submitter import Submitter
from pydra.utils.messenger import AuditFlag, FileMessenger
import os

#####################################################################
DATASET = "abide2"
SITE = "BNI_1"

BASE = "/om2/scratch/Thu/nlo"
DATADIR = f"/BASE/{DATASET}/{SITE}"
OUTDIR = f"/BASE/{DATASET}/{SITE}/derivatives"
CACHEDIR = f"{BASE}/pydra-cache/{DATASET}/{SITE}"

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
SUBJECTS= SUBJECTS[:2] # testing
print(f"SUBJECTS = {SUBJECTS}")
CMD_LIST = list()


for s in SUBJECTS:

    SUBWORKDIR = f"/BASE/fmriprep-workdir/{DATASET}/{SITE}/{s}"
    if not os.path.exists(SUBWORKDIR.replace("/BASE", BASE)):
        os.makedirs(SUBWORKDIR.replace("/BASE", BASE))

    #--fs-license-file {FS_LICENSE} \
    CMD = f"fmriprep {DATADIR} {OUTDIR} \
    participant --participant_label {s} --nprocs 2 \
    --output-space fsaverage6 --use-aroma \
    --skip-bids-validation --mem_mb 7500 \
    --fs-license-file /BASE/freesurfer_license.txt \
    --fs-subjects-dir {OUTDIR}/freesurfer \
    --ignore slicetiming --cifti-output -w {SUBWORKDIR}".split()
    CMD_LIST.append(CMD)

print("Sample command:")
print(CMD_LIST[0])

#####################################################################
singu = SingularityTask(
    name="fmriprep",
    executable=CMD_LIST,
    image=IMAGE,
    cache_dir=CACHEDIR,
    bindings=[(BASE, "/BASE", "rw")],
    container_xargs=['--cleanenv'],
    #audit_flags=AuditFlag.ALL,
    #messenger=FileMessenger()
).split("executable")

print()
print("SingularityTask inputs:")
print(singu.inputs)
print()
print("SingularityTask container_args:")
print(singu.container_args)
print()

SBATCH_ARGS = f"-J {SITE} -t 30:00:00 --mem=8GB --cpus-per-task=2 -p normal"
print(f"sbatch_args:{SBATCH_ARGS}")

print("SUBMITTER FORMAT - NO CONTEXT MANAGER")
print("sub = Submitter(plugin='slurm', sbatch_args=SBATCH_ARGS, max_jobs=400)")
print("task(submitter=sub)")	

sub = Submitter(plugin="slurm", sbatch_args=SBATCH_ARGS, max_jobs=400)
singu(submitter=sub)


print("Done running!")
#print(f"res.output.stdout = {res.output.stdout}")
#print()
#print(f"res.output.return_code = {res.output.return_code}")
