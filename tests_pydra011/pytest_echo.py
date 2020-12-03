import os, shutil
import subprocess as sp
import pytest
import attr
import time

from pydra.engine.task import SingularityTask, FunctionTask
from pydra.engine.submitter import Submitter


need_singularity = pytest.mark.skipif(
    shutil.which("singularity") is None, reason="no singularity available"
)

#####################################################################

JOB_SBATCH_ARGS = "-t 1-00:00 --mem=4GB --cpus-per-task=4 -p gablab"
LIST_LENS = [1, 2, 3, 8, 30, 100]
#IMAGE="/om4/group/gablab/data/singularity-images/test/mriqc-v.0.15.1.sif"
#IMAGE = "/net/vast-storage.ib.cluster/scratch/Thu/nlo/datalad-v0.12.7.sif"
#IMAGE = 'fmriprep-20.2.0.sif'
#IMAGE = 'datalad-v0.12.7.sif'
#IMAGE = "library://sylabsed/linux/alpine"
#IMAGE="docker://poldracklab/fmriprep:20.2.0"
#IMAGE = "/net/vast-storage.ib.cluster/scratch/Thu/nlo/fmriprep-20.2.0.sif"
#IMAGE = "/net/vast-storage.ib.cluster/scratch/Thu/nlo/alpine_latest.sif"
#IMAGE = "/om4/group/gablab/data/singularity-images/alpine_latest.sif"
IMAGE="/om4/group/gablab/data/singularity-images/fmriprep-20.2.0.sif"
#IMAGE = "/om4/group/gablab/data/singularity-images/datalad-v0.12.7.sif"
PLUGIN = "slurm"
N_PROCS = None  # None for default
#N_PROCS=10

#####################################################################


@need_singularity
def test_echo(
    tmpdir,
    plugin=PLUGIN,
    list_lens=LIST_LENS,
    job_sbatch_args=JOB_SBATCH_ARGS,
    image=IMAGE,
    n_procs=N_PROCS,
):
    """no splitting, no result"""
    print("Linux container, no bind, splitting on echo")
    print("--------------------------------------------------")
    print("Singularity Task arguments:")
    print(f"image == {image}")
    print(f"tmpdir == {str(tmpdir)}")

    cmd = "echo"
    print(f"cmd == {cmd}")
    print()
    print("--------------------------------------------------")
    print("Submitter args")
    print(f"job_sbatch_args == {job_sbatch_args}")
    print(f"plugin == {plugin}")
    print(f"n_procs == {n_procs}")
    image = image

    args = dict()
    for i in list_lens:
        if i == 1:
            args = str(1)
        else:
            args = [str(i) for i in range(1, i + 1)]

        sub_tmpdir = str(tmpdir.join(f"fmriprep_echo{i}"))
        singu = SingularityTask(
            name=f"fp{i}", executable=cmd, args=args, image=image, cache_dir=tmpdir
        )
        # singu = FunctionTask(name='ft', executable=cmd, args=args, cache_dir=tmpdir)
        if isinstance(args, list):
            singu.split("args")

        print()
        print(f"Submitting job with {i} split(s)...")
        t0 = time.time()
        with Submitter(plugin=plugin, sbatch_args=job_sbatch_args, n_procs=n_procs) as sub:
            # with Submitter(plugin='cf') as sub:
            singu(submitter=sub)
        t1 = time.time()
        print(f"Time to submit: {t1-t0} s")
