import pydra
from pydra.engine.task import ShellCommandTask
from pydra.engine.submitter import Submitter


# result_submitter in utils.py
def result_function(shell_task, plugin):
    with Submitter(plugin=plugin) as sub:
            shell_task(submitter=sub)
    return shell_task.result()


cmd = ["echo"]
args = ["hello", "hi"]

shelly = ShellCommandTask(name="shelly", executable=cmd, args=args)

res = result_function(shelly, 'slurm')
print(f'res.output == {res.output}')
assert res.output == "hello hi"

print("end!")
