#!/om2/user/nlo/miniconda/envs/pydra/bin/python

import os, sys, argparse


def submit_task_test(argv):

	parser = argparse.ArgumentParser()
	parser.add_argument('-c', '--command', metavar='command', help="fmriprep command")
	parser.add_argument('-i', '--image', metavar='image_path', help="fmriprep image path")
	parser.add_argument('-pc', '--pydra_cache' ,metavar='pydra-cache',  help="path to store pydra cache")
	parser.add_argument('-b', '--base', help="base path of BIDS dataset")
	parser.add_argument('-sa', '--sbatch_args', help="SBATCH args")

	args = parser.parse_args()
	#print('inside run_test.py')
	print(args.command)
	with open('test.txt', 'a') as f:
		f.write('inside run_test.py!!!!\n')
		f.write(args.command)
		f.write('\n\n')



submit_task_test(sys.argv[1:])
