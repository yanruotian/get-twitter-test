import sys

def main():
    num = sys.argv[1]
    return f'{int(num) :2d}'.replace(' ', '0')

if __name__ == '__main__':
    print(main())
    