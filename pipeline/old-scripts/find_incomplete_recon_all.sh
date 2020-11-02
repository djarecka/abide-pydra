#!/bin/bash

# Iterate through ABIDE I/II subject mindboggle output directories to find which subjects did not ran properly

root=/scratch/Thu/nlo/
dataset=abide
site=CMU_a
fs_dir=$root/$dataset/$site/derivatives/freesurfer

incomplete_log=${dataset}-${site}-incomplete-recon-all.log
touch $incomplete_log
complete_log=${dataset}-${site}-complete-recon-all.log
touch $complete_log

# find all subjects
pushd $fs_dir
subjs=($(ls -d sub-*))
echo ${subjs[@]}
popd


for s in ${subjs[@]}; do
    file="${fs_dir}/${s}/scripts/recon-all-status.log"
    if [ ! -f $file ]; then
        echo "$s missing recon-all-status.log"
        exit 1
    else
	string="$(tail -n 2 $file)" # contains completion status
	
	# save subjects in co files 
        if [[ $string == *"exited with ERRORS"* ]]; then
            echo $s exited with erors
	    echo $s >> $incomplete_log
        else
	    echo $s >> $complete_log
	fi
    fi
done
        

#echo $(cat lists/fs_error_subjs
