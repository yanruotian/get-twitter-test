#! /usr/bin/bash

# 原始大小：110,570,338,625 字节（约102GB）
# 后来大小：132,256,781,235 字节（约123GB）
# 11-05-06-50 ~ 11-06-10-36 约1670分钟
# 0.7545 GB/h

# CONDA_ACTIVATE="/home/yanruotian/miniconda3/bin/activate"
# source ${CONDA_ACTIVATE} python3.8
# which python3.8

BASE_DIR="/root/get-twitter-test"
SCI_DIR="${BASE_DIR}/Sci"
TRANSFORM_DIR="${BASE_DIR}/transformed-sci"
DIVIDE_DIR="${BASE_DIR}/divided-sci"
DOWNLOAD_DIR="${BASE_DIR}/downloaded-sci"

process_num=32

do_transform=yes
do_divide=yes
do_download=yes

# transform id txts to content txts
if [ "$do_transform" == "yes" ]; then
    echo "doing transform..."
    python3 -m code \
        --mode transform --load_path "${SCI_DIR}" \
        --output_path "${TRANSFORM_DIR}" \
        --log_path "${TRANSFORM_DIR}/transform.log"
fi

# divide content txts into process txts
# this step also removes same contents
if [ "$do_divide" == "yes" ]; then
    echo "doing divide..."
    python3 -m code \
        --mode divide --load_path "${TRANSFORM_DIR}" \
        --output_path "${DIVIDE_DIR}" -n ${process_num} \
        --log_path "${DIVIDE_DIR}/divide.log"
fi

# download search contents according to divided txts
if [ "$do_download" == "yes" ]; then
    echo "doing download, process num = ${process_num}..."
    process=0
    while [ ${process} -lt ${process_num} ]; do
        process_string=$(python3 trans_num.py ${process})
        echo "process ${process_string} started..."
        python3 -m code \
            --mode download --load_path "${DIVIDE_DIR}" \
            --output_path "${DOWNLOAD_DIR}/${process_string}" -n ${process} \
            --log_path "${DOWNLOAD_DIR}/download-${process_string}.log" &
        ((process=${process}+1))
    done
fi

wait
