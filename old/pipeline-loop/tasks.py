import os

# Given a dataset (and optionally site), list all subjects
# TODO optional subject argument
def get_subjects(base_path, dataset, site):
    datadir = os.path.join(base_path, dataset, site)
    subjects = [
        s
        for s in os.listdir(datadir)
        if (s.startswith("sub-") and os.path.isdir(os.path.join(datadir, s)))
    ]
    return subjects


# for one subject
def create_fmriprep_cmd(
    base,
    dataset,
    site,
    subject,  # from loop
    workdir=None,
    fs_license=None,
    nthreads=1,
    mem_mb=9500,
    **kwargs,
):

    # assuming base_path is binded to the container as '/BASE'
    wd = os.path.join(base, workdir, dataset, site)
    if not os.path.exists(wd):
        os.makedirs(wd)

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
