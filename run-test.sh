TEST_DIR="/root/get-twitter-test/test"
DIVIDE_DIR="${TEST_DIR}/pooled"

for mode in "threaded-download"; do 
    BASE_DIR="${TEST_DIR}/${mode}"
    DOWNLOAD_DIR="${BASE_DIR}"
    process_num=32
    python3 -m code \
        --mode ${mode} --load_path "${DIVIDE_DIR}" \
        --output_path "${DOWNLOAD_DIR}/downloaded" -n ${process_num} \
        --log_path "${DOWNLOAD_DIR}/download.log" 
done
