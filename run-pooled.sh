#! /usr/bin/bash

# CONDA_ACTIVATE="/home/yanruotian/miniconda3/bin/activate"
# source ${CONDA_ACTIVATE} python3.8
# which python3.8

BASE_DIR="/root/get-twitter-test"
DIVIDE_DIR="${BASE_DIR}/pooled"
DOWNLOAD_DIR="${BASE_DIR}/downloaded-pooled-tec"

process_num=32

python3 -m code \
    --mode pooled-download --load_path "${DIVIDE_DIR}" \
    --output_path "${DOWNLOAD_DIR}/downloaded" -n ${process_num} \
    --log_path "${DOWNLOAD_DIR}/pooled-download.log" 
