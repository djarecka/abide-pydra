# run ABIDE workflow
# abide pydra pipeline
# run with /om2/user/nlo/miniconda/envs/pydra/bin/python run.py
from tasks import get_subjects, create_fmriprep_cmd
import os
import time
import subprocess

#####################################################################
# specify inputs

BASE = "/Users/gablab/Desktop/nlo/openmind/abide-pydra" #"/scratch/Thu/nlo" # "/Users/gablab/Desktop/nlo/openmind/abide-pydra"
DATASET = "abide2"
SITES = "UCLA_Long"

IMAGE = "/om4/group/gablab/data/singularity-images/fmriprep-v1.3.0p2.sif"
PYDRA_CACHE = "/Users/gablab/Desktop/nlo/openmind/abide-pydra/pydra-cache" #"/scratch/Thu/nlo/pydra-cache" 
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
        subjects = get_subjects(base, dataset, site)
        print(f"subjects: {subjects}")

        for sub in subjects:
            fmriprep_cmd = create_fmriprep_cmd(base, dataset, site, sub, **fmriprep_args)
            sub_sbatch_args = f"-J {site}-{sub} " + sbatch_args
            sub_pydra_cache = os.path.join(cache_dir, dataset, site, sub)
            if not os.path.exists(sub_pydra_cache):
                os.makedirs(sub_pydra_cache)

            # run each task as subprocess
            script = "run_fmriprep.py"
            run_script_cmd = f'python {script} -c {fmriprep_cmd} -i {image} -pc {sub_pydra_cache} \
            -b {base} -sa {sub_pydra_cache} &'
            #run_script_cmd = f"echo hello {site} {sub}"
            p = subprocess.Popen(run_script_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                close_fds=True, shell=True)
            print(f'Running run_fmriprep.py for {sub}')

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
        sbatch_args=SBATCH_ARGS,
        fmriprep_args=FMRIPREP_ARGS,
    )
)
