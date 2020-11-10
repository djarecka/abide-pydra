import pydra
from pydra.engine.task import SingularityTask, ShellCommandTask
from pydra.engine.submitter import Submitter
from pydra.engine.core import Workflow

import os

#####################################################################
# Create pydra tasks
@pydra.mark.task
def get_subject(base_path, dataset, site):
    datadir = os.path.join(base_path, dataset, site)
    subjects = [
        s
        for s in os.listdir(datadir)
        if (s.startswith("sub-") and os.path.isdir(os.path.join(datadir, s)))
    ]
    return ["sub-0050574", "sub-0050575", "sub-0050576"]
    # return subjects


# for one subject
@pydra.mark.task
def create_fmriprep_cmd(
    base_path,
    dataset,
    site,
    subject,  # from loop
    workdir=None,
    fs_license=None,
    nthreads=1,
    mem_mb=9500,
    **kwargs,
):

    # create separate working directory for each subject
    wd = os.path.join(base_path, workdir, dataset, site, subject)
    if not os.path.exists(wd):
        os.makedirs(wd)

    # assuming base_path is binded to the container as '/BASE'
    datadir_template = os.path.join("/BASE", dataset, site)
    outdir_template = os.path.join("/BASE", dataset, site, "derivatives")
    workdir_template = os.path.join("/BASE", workdir, dataset, site, subject)

    cmd = f"fmriprep {datadir_template} {outdir_template} \
    -w {workdir_template} participant --participant_label {subject} \
    --nthreads {nthreads} --output-space fsaverage6 \
    --use-aroma --ignore-aroma-denoising-errors \
    --skip-bids-validation --mem_mb {mem_mb} --fs-license-file {fs_license} \
    --ignore slicetiming --cifti-output".split()

    return cmd


#####################################################################

wf_inputs = {
    "base_path": "/scratch/Thu/nlo",  # "/Users/gablab/Desktop/nlo/openmind/abide-pydra",
    "dataset": "abide2",
    "site": "UCLA_Long",
    "fs_license": "/home/nlo/.freesurfer_license.txt",
    "workdir": "fmriprep-workdir",
}


wf = Workflow(name="wf", input_spec=list(wf_inputs.keys()), **wf_inputs)
# subjects from same site uses one pydra cache
pydra_cache = "/scratch/Thu/nlo/pydra-cache/{dataset}/{site}".format(**wf_inputs)
# pydra_cache = "/Users/gablab/Desktop/nlo/openmind/abide-pydra/pydra-cache/{dataset}/{site}".format(
#    **wf_inputs
# )
if not os.path.exists(pydra_cache):
    os.makedirs(pydra_cache)
wf.cache_dir = pydra_cache


wf.add(
    get_subject(
        name="get_subject",
        base_path=wf.lzin.base_path,
        dataset=wf.lzin.dataset,
        site=wf.lzin.site,
    )
)
wf.add(
    create_fmriprep_cmd(
        name="create_cmd",
        subject=wf.get_subject.lzout.out,
        base_path=wf.lzin.base_path,
        dataset=wf.lzin.dataset,
        site=wf.lzin.site,
        fs_license=wf.lzin.fs_license,
        workdir=wf.lzin.workdir,
    ).split("subject")
)
wf.set_output([("out", wf.create_cmd.lzout.out)])

with Submitter(plugin="cf") as sub:
    sub(wf)

res = wf.result()
cmd_list = res.output.out

# wf2 = Workflow(name="wf2", input_spec=['executable', 'image'])
singu = SingularityTask(
    name="fmriprep",
    executable=cmd_list,
    image="/om4/group/gablab/data/singularity-images/fmriprep-v1.3.0p2.sif",
    bindings=[(wf_inputs["base_path"], "/BASE", "rw")],
).split("executable")


# set fmriprep commands as workflow output for now
# wf.set_output([("out", wf.fmriprep.lzout.stdout),
#                ("err", wf.fmriprep.lzout.stderr)])

sbatch_args = "-J {site} -t 1-00:00:00 --mem=10GB --cpus-per-task=1".format(**wf_inputs)
with Submitter(plugin="slurm", sbatch_args=sbatch_args) as sub:
    sub(singu)
