# run ABIDE workflow
# abide pydra pipeline
# run with /om2/user/nlo/miniconda/envs/pydra/bin/python run.py
from pydra.engine.task import SingularityTask
from pydra.engine.submitter import Submitter
from pydra.utils.messenger import FileMessenger, AuditFlag

from tasks import get_subjects, create_fmriprep_cmd
import os
import time

#####################################################################
# specify inputs

BASE = "/scratch/Thu/nlo" # "/Users/gablab/Desktop/nlo/openmind/abide-pydra"
DATASET = "abide2"
SITES = "UCLA_Long"

IMAGE = "/om4/group/gablab/data/singularity-images/fmriprep-v1.3.0p2.sif"
PYDRA_CACHE = "/scratch/Thu/nlo/pydra-cache" #"/Users/gablab/Desktop/nlo/openmind/abide-pydra/pydra-cache"
SBATCH_ARGS = "--time 1-00:00:00 --mem=10GB --cpus-per-task=1"

FMRIPREP_ARGS = dict(
    workdir="fmriprep-workdir", fs_license="/home/nlo/.freesurfer_license.txt"
)

#####################################################################
# Create pydra tasks


def gen_tasks(
    base=BASE,
    dataset=DATASET,
    sites=SITES,
    image=IMAGE,
    cache_dir=PYDRA_CACHE,
    cache_locations=None,
    sbatch_args=SBATCH_ARGS,
    fmriprep_args=FMRIPREP_ARGS,
):

    if sites is None:
        sites = [
            s for s in os.listdir(os.path.join(base, dataset)) if not s.startswith(".")
        ]
    if isinstance(sites, str):
        sites = [sites]
    print(sites)

    for site in sites:
        print(f"SITE: {site}")
        print(f"base: {base}")
        subjects = get_subjects(base, dataset, site)

        for sub in subjects:
            cmd = create_fmriprep_cmd(base, dataset, site, sub, **fmriprep_args)
            sub_sbatch_args = f"-J {site}-{sub} " + sbatch_args
            sub_pydra_cache = os.path.join(cache_dir, dataset, site, sub)
            if not os.path.exists(sub_pydra_cache):
                os.makedirs(sub_pydra_cache)

            print(f"{sub}")
            print(f"cmd == {cmd}")
            print(f"sub_sbatch_args == {sub_sbatch_args}")
            print(f"sub_pydra_cache == {sub_pydra_cache}")
            print()
            print()

            singu = SingularityTask(
                name="fmriprep",
                executable=cmd,
                image=image,
                cache_dir=sub_pydra_cache,
                cache_locations=cache_locations,
                audit_flags=AuditFlag.ALL,
                messengers=FileMessenger(),
                messenger_args={"message_dir": os.path.join(os.getcwd(), "messages")},
                bindings=[(BASE, "/BASE", "rw")],
            )

            with Submitter(plugin="slurm", sbatch_args=sub_sbatch_args) as submit:
                singu(submitter=submit)

        # wait for a bit after each site is submitted so SLURM won't get overwhelmed
        print("pause between sites")
        time.sleep(10)


#####################################################################
# Run
print(
    gen_tasks(
        base=BASE,
        dataset=DATASET,
        sites=SITES,
        image=IMAGE,
        cache_dir=PYDRA_CACHE,
        cache_locations=None,
        sbatch_args=SBATCH_ARGS,
        fmriprep_args=FMRIPREP_ARGS,
    )
)
