singularity exec -B /om2/scratch/Thu/nlo:/BASE:rw \
 fmriprep-20.2.0.sif fmriprep /BASE/abide/KKI \
 /BASE/abide/KKI/derivatives participant --participant_label sub-0050776 \
 -w /BASE/fmriprep-workdir/abide/KKI/sub-0050776 --skip-bids-validation \
 --fs-license-file /BASE/freesurfer_license.txt \
 --fs-subjects-dir /BASE/abide/KKI/derivatives



unset FREESURFER_HOME; singularity exec -B /om2/scratch/Thu/nlo:/BASE:rw \
 /om4/group/gablab/data/singularity-images/fmriprep-v1.3.0p2.sif \
  fmriprep /BASE/abide/KKI \
 /BASE/abide/KKI/derivatives participant --participant_label sub-0050778 \
 -w /BASE/fmriprep-workdir/abide/KKI/sub-0050778 --skip-bids-validation \
 --fs-license-file /BASE/freesurfer_license.txt 

# WORKING!

singularity exec --cleanenv -B /om2/scratch/Thu/nlo:/BASE:rw fmriprep-20.2.0.sif fmriprep /BASE/abide/KKI /BASE/abide/KKI/derivatives participant --participant_label sub-0050775 -w /BASE/fmriprep-workdir/abide/KKI/sub-0050775 --skip-bids-validation --fs-license-file /BASE/freesurfer_license.txt
