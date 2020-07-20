import os
import argparse

f_dir = os.path.abspath(os.path.dirname(__file__))

def get_dir_size(dir):
    size = 0
    for root, dirs, files in os.walk(dir):
        size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
    return size

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', required=True)
    args = parser.parse_args()
    path = args.path
    
    size = get_dir_size(path)
    print('Total size is: %.3f Mb'%(size/1024/1024))
