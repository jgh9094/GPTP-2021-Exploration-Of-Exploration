#!/bin/bash

EXP_TAG=2021-06-01-novelty
EXP_DIR=/mnt/home/lalejini/devo_ws/GPTP-2021/experiments
BASE_DATA_DIR=/mnt/scratch/lalejini/data/gptp-2021/${EXP_TAG}

REPLICATES=50
CONFIG_DIR=${EXP_DIR}
JOB_DIR=${BASE_DATA_DIR}/jobs
# JOB_DIR=./

python3 gen-sub.py --data_dir ${BASE_DATA_DIR} --config_dir ${CONFIG_DIR} --replicates ${REPLICATES} --job_dir ${JOB_DIR}