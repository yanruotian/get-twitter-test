# 用于多进程调用twsrc模块，测试速度是否会有提升。

export PYTHONPATH="$PYTHONPATH:/root/get-twitter-test"

ROOT_PATH="/root/get-twitter-test/tw-multi"
KEYWORDS_FILE_NAME="keywords-date"
KEYWORDS="/root/get-twitter-test/keywords/china-tec-new2/$KEYWORDS_FILE_NAME"
# ACCOUNTS="/root/get-twitter-test/tw-multi/accounts-new-2.txt"
# PROXIES="/root/get-twitter-test/tw-multi/proxies-new.txt"
P_NUM=24
OUTPUT_DIR="splits"

# rm -r $OUTPUT_DIR

# python3 split.py -i $ACCOUNTS -o $OUTPUT_DIR -n $P_NUM
# python3 split.py -i $PROXIES -o $OUTPUT_DIR -n $P_NUM
# python3 split.py -i $KEYWORDS -o $OUTPUT_DIR -n $P_NUM

# <<'COMMENT'
function download() {
    export LOG_FILE=tw.log
    python3 -m twsrc \
        --accounts accounts-new-2.txt \
        --keywords $KEYWORDS_FILE_NAME \
        --proxies proxies-new.txt \
        --output downloaded
}

i=0
while [ $i -lt $P_NUM ]; do
    dir=$(printf "splits/split-%02d" $i)
    cd $ROOT_PATH/$dir
    download &
    ((i=$i+1))
done  

wait
# COMMENT
