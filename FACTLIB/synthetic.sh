#!/bin/bash

#SBATCH --mail-type=ALL                           # mail configuration: NONE, BEGIN, END, FAIL, REQUEUE, ALL
#SBATCH --output=log/%j.out     # where to store the output (%j is the JOBID), subdirectory "log" must exist
#SBATCH --error=log/%j.err  # where to store error messages
#SBATCH --cpus-per-task=32

# Exit on errors
set -o errexit

# Set a directory for temporary files unique to the job with automatic removal at job termination
TMPDIR=$(mktemp -d)
if [[ ! -d ${TMPDIR} ]]; then
    echo 'Failed to create temp directory' >&2
    exit 1
fi

trap "exit 1" HUP INT TERM
trap 'rm -rf "${TMPDIR}"' EXIT
export TMPDIR

# Adapt this to your personal preference
# cd "${TMPDIR}" || exit 1

# Send some noteworthy information to the output log
echo "Running on node: $(hostname)"
echo "In directory:    $(pwd)"
echo "Starting on:     $(date)"
echo "SLURM_JOB_ID:    ${SLURM_JOB_ID}"

# Binary or script to execute
python synthetic_dataset.py

# Send more noteworthy information to the output log
echo "Finished at:     $(date)"

# End the script with exit code 0
exit 0