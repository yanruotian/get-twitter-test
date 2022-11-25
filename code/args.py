from argparse import ArgumentParser, Namespace

def get_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument(
        '--mode', type = str, default = 'download', 
        choices = ['download', 'transform', 'divide']
    )
    parser.add_argument('--load_path', type = str, default = '')
    parser.add_argument('--output_path', type = str, default = '')
    parser.add_argument('--log_path', type = str, default = '')
    parser.add_argument('-n', type = int, default = 0)
    return parser.parse_args() 
    