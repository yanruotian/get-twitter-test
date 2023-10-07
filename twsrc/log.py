import logging

def info(*msg: str):
    print(*msg)
    logging.info(*msg)
    