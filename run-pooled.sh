#! /usr/bin/bash

# CONDA_ACTIVATE="/home/yanruotian/miniconda3/bin/activate"
# source ${CONDA_ACTIVATE} python3.8
# which python3.8

BASE_DIR="."
DIVIDE_DIR="${BASE_DIR}/keywords/china-tec-new"
DOWNLOAD_DIR="${BASE_DIR}/downloaded/china-tec-new-2023-05-12"

process_num=32

python3 -m src \
    --mode pooled-download --load_path "${DIVIDE_DIR}" \
    --output_path "${DOWNLOAD_DIR}/downloaded" -n ${process_num} \
    --log_path "${DOWNLOAD_DIR}/pooled-download.log" \
    2>&1 | tee 2023-05-12.log
