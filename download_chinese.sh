#! /usr/bin/bash

DOWNLOAD_DIR="download-chinese"
process_string="00"

python3 -m code \
    --mode download --load_path "chinese" \
    --output_path "${DOWNLOAD_DIR}/${process_string}" -n 0 \
    --log_path "${DOWNLOAD_DIR}/download-${process_string}.log" 
