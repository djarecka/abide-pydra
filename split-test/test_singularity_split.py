import os, shutil
import subprocess as sp
import pytest
import attr

from ..task import SingularityTask, DockerTask, ShellCommandTask
from ..submitter import Submitter
from ..core import Workflow
from ..specs import ShellOutSpec, SpecInfo, File, SingularitySpec


need_singularity = pytest.mark.skipif(
    shutil.which("singularity") is None, reason="no singularity available"
)

#####################################################################

fmriprep_inputs = {
    "base_path": "/scratch/Thu/nlo",  # "/Users/gablab/Desktop/nlo/openmind/abide-pydra",
    "dataset": "abide2",
    "site": "USM",
    "fs_license": ".freesurfer_license.txt",
    "workdir": "fmriprep-workdir",
}



#####################################################################
# Run with linux/alphine

@need_singularity
def test_singularity_linux_1(plugin, tmpdir):
    """ split commands
    	linux container, no binding
    """
    cmd = ["pwd", "ls", "echo", "wc", "lh", "ss", "aw", "aa", "lk"]
    image = "library://sylabsed/linux/alpine"
    singu = SingularityTask(
        name="singu", executable=cmd, image=image, cache_dir=tmpdir
    ).split("executable")
    assert singu.state.splitter == "singu.executable"

    res = singu(plugin=plugin)


@need_singularity
def test_singularity_linux_2(plugin, tmpdir):
    """ command with arguments in docker, checking the distribution
        splitter = image
    """
    cmd = ["pwd", "ls", "echo", "wc", "lh", "ss", "aw", "aa", "lk"]
    image = "library://sylabsed/linux/alpine"
    singu = SingularityTask(
        name="singu", 
        executable=cmd, 
        image=image, 
        cache_dir=tmpdir,
        bindings=[(fmriprep_inputs["base_path"], "/BASE", "rw")],
    ).split("cmd")
    assert singu.state.splitter == "singu.executable"

    res = singu(plugin=plugin)




@need_singularity
def test_singularity_fmriprep_1(plugin, tmpdir):
    """ split commands
    	fmriprep container, no binding
    """
    cmd = ["pwd", "ls", "echo", "wc", "lh", "ss", "aw", "aa", "lk"]
    image = "/om4/group/gablab/data/singularity-images/fmriprep-v1.3.0p2.sif"
    singu = SingularityTask(
        name="singu", executable=cmd, image=image, cache_dir=tmpdir
    ).split("executable")
    assert singu.state.splitter == "singu.executable"

    res = singu(plugin=plugin)


@need_singularity
def test_singularity_fmriprep_2(plugin, tmpdir):
    """ command with arguments in docker, checking the distribution
        splitter = image
    """
    cmd = ["pwd", "ls", "echo", "wc", "lh", "ss", "aw", "aa", "lk"]
    image = "/om4/group/gablab/data/singularity-images/fmriprep-v1.3.0p2.sif"
    singu = SingularityTask(
        name="singu", 
        executable=cmd, 
        image=image, 
        cache_dir=tmpdir,
        bindings=[(fmriprep_inputs["base_path"], "/BASE", "rw")],
    ).split("cmd")
    assert singu.state.splitter == "singu.executable"

    res = singu(plugin=plugin)
