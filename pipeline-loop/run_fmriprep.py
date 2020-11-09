#!/om2/user/nlo/miniconda/envs/pydra/bin/python
# run fmriprep container in background

from pydra.engine.task import SingularityTask
from pydra.engine.submitter import Submitter
from pydra.utils.messenger import FileMessenger, AuditFlag
import os, sys, argparse


def submit_task(argv):

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--command', metavar='command', help="fmriprep command")
    parser.add_argument('-i', '--image', metavar='image_path', help="fmriprep image path")
    parser.add_argument('-pc', '--pydra_cache' ,metavar='pydra-cache',  help="path to store pydra cache")
    parser.add_argument('-b', '--base', help="base path of BIDS dataset")
    parser.add_argument('-sa', '--sbatch_args', help="SBATCH args")

    args = parser.parse_args()
    print(args.command)

    singu = SingularityTask(
                name="fmriprep",
                executable=args.command,
                image=args.image,
                cache_dir=args.pydra_cache,
                audit_flags=AuditFlag.ALL,
                messengers=FileMessenger(),
                messenger_args={"message_dir": os.path.join(args.base, "messages")},
                bindings=[(args.base, "/BASE", "rw")],
            )
    with Submitter(plugin="slurm", sbatch_args=args.sbatch_args) as sb:
        singu(submitter=sb)


if __name__ == "__main__":
    print(submit_task(sys.argv[1:]))
