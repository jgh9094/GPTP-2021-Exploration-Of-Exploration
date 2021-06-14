#!/bin/bash

EXP_TAG=2021-06-14-downsampled-pop-size
EXP_DIR=/mnt/home/lalejini/devo_ws/GPTP-2021/Hpcc/aml-reruns
BASE_DATA_DIR=/mnt/scratch/lalejini/data/gptp-2021/${EXP_TAG}

REPLICATES=50
CONFIG_DIR=${EXP_DIR}
JOB_DIR=${BASE_DATA_DIR}/jobs

python3 gen-sub.py --data_dir ${BASE_DATA_DIR} --config_dir ${CONFIG_DIR} --replicates ${REPLICATES} --job_dir ${JOB_DIR}