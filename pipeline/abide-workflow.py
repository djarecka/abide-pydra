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
    return subjects


@pydra.mark.task
def create_cmd(
    base_path,
    dataset,
    site,
    subject,
    fs_license,
    base_name="BASE",
    datadir_template=None,
    outdir_template=None,
    workdir_template=None,
    nthreads=4,
    output_space="fsaverage6",
    mem_mb=7800,
):

    # assuming base_path is binded to the container as '/BASE' or base_name
    if not workdir_template:
        workdir_template = os.path.join(base_name, "fmriprep_work_dir")
    if not datadir_template:
        datadir_template = os.path.join(base_name, dataset, site)
    if not outdir_template:
        outdir_template = os.path.join(base_name, dataset, site, "deriviatives")

    if not outdir_template.replace(base_name, base_path):
        os.makedirs(outdir_template.replace(base_name, base_path))

    cmd = f"fmriprep {datadir_template} {outdir_template} \
    -w {workdir_template} participant --participant_label {subject} \
    --nthreads {nthreads} --output-space {output_space} \
    --use-aroma --ignore-aroma-denoising-errors \
    --skip-bids-validation --mem_mb {mem_mb} --fs-license-file {fs_license} \
    --ignore slicetiming --cifti-output".split(
        " "
    )

    return cmd


wf_inputs = {
    "base_path": "/scratch/Thu/nlo",
    "dataset": "test-data",
    "site": "Yale-pydra",
    "fs_license": "/home/nlo/.freesurfer_license.txt",
    "image_path": "/om4/group/gablab/data/singularity-images/fmriprep-v1.3.0p2.sif",
}


wf = Workflow(name="wf", input_spec=list(wf_inputs.keys()), **wf_inputs)
wf.cache_dir = "/scratch/Thu/nlo/pydra_cache_dir"

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
        bindings=[(BASE, "/BASE", "rw")],
    ).split("executable")
)

wf.set_output([("out", wf.fmriprep.lzout.out)])

sbatch_args = "-J abide-fmriprep -t 16:00:00 --mem=8GB --cpus-per-task=4"
with Submitter(plugin="slurm", sbatch_args=sbatch_args) as sub:
    sub(wf)

results = wf.result()
print(results.output.out)
