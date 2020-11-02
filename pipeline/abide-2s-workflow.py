import pydra
from pydra.engine.task import SingularityTask, ShellCommandTask
from pydra.engine.submitter import Submitter
from pydra.engine.core import Workflow

import os


@pydra.mark.task
def get_subject(base_path, dataset, site):
    datadir = os.path.join(base_path, dataset, site)
    subjects = [
        s
        for s in os.listdir(datadir)
        if (s.startswith("sub-") and os.path.isdir(os.path.join(datadir, s)))
    ]
    return ['sub-0050625', 'sub-0050626']
#    return subjects


@pydra.mark.task
def create_cmd(
    base_path,
    dataset,
    site,
    subject,
    fs_license,
    datadir=None,
    outdir=None,
    workdir=None,
    nthreads=4,
    output_space="fsaverage6",
    mem_mb=11000,
):

    # assuming base_path is binded to the container as '/BASE' or base_name
    if not datadir:
        datadir = f"/BASE/{dataset}/{site}"
    if not outdir:
        outdir = f"/BASE/{dataset}/{site}/derivatives"
    if not workdir:
        workdir = f"/BASE/fmriprep_work_dir"

    cmd = f"fmriprep {datadir} {outdir} \
    -w {workdir} participant --participant_label {subject} \
    --nthreads {nthreads} --output-space {output_space} \
    --use-aroma --ignore-aroma-denoising-errors \
    --skip-bids-validation --mem_mb {mem_mb} --fs-license-file {fs_license} \
    --ignore slicetiming --cifti-output".split()

    return cmd


wf_inputs = {
    "base_path": "/scratch/Thu/nlo",
    "dataset": "abide",
    "site": "Yale",
    "fs_license": "/home/nlo/.freesurfer_license.txt",
    "image_path": "/om4/group/gablab/data/singularity-images/fmriprep-v1.3.0p2.sif",
}


wf = Workflow(name="wf", input_spec=list(wf_inputs.keys()), **wf_inputs)
# hard coding cache_dir for now
wf.cache_dir = "/scratch/Thu/nlo/pydra_cache_dir/20201101-Yale-0050625-6" 

wf.add(
    get_subject(
        name="get_subject",
        base_path=wf.lzin.base_path,
        dataset=wf.lzin.dataset,
        site=wf.lzin.site,
    )
)
wf.add(
    create_cmd(
        name="create_cmd",
        subject=wf.get_subject.lzout.out,
        base_path=wf.lzin.base_path,
        dataset=wf.lzin.dataset,
        site=wf.lzin.site,
        fs_license=wf.lzin.fs_license,
    ).split("subject")
)

wf.add(
    SingularityTask(
        name="fmriprep",
        executable=wf.create_cmd.lzout.out,
        image=wf.lzin.image_path,
        bindings=[(wf_inputs['base_path'], "/BASE", "rw")],
    )
)

# set fmriprep commands as workflow output for now
wf.set_output([("out", wf.fmriprep.lzout.stdout),
               ("err", wf.fmriprep.lzout.stderr)])

sbatch_args = "-J s50625-6 -t 1-00:00:00 --mem=12GB --cpus-per-task=4"
with Submitter(plugin="slurm", sbatch_args=sbatch_args) as sub:
    sub(wf)
