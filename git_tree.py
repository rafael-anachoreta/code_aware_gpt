import os
import subprocess
import utils

def get_git_files(path):
    result = subprocess.run(['git', '-C', path, 'ls-files'], stdout=subprocess.PIPE, text=True, cwd=path)
    files = result.stdout.splitlines()
    return files

def build_tree(files):
    tree = {}
    for file in files:
        parts = file.split('/')
        current = tree
        for part in parts:
            if part not in current:
                current[part] = {}
            current = current[part]
    return tree

def print_tree(tree, prefix=''):
    items = list(tree.items())
    for index, (key, value) in enumerate(sorted(items)):
        if index == len(items) - 1:  # Last item
            print(f"{prefix}└── {key}")
            if value:
                print_tree(value, prefix + "    ")
        else:
            print(f"{prefix}├── {key}")
            if value:
                print_tree(value, prefix + "│   ")

def main():
    path = utils.target_directory
    if not os.path.isabs(path):
        path = os.path.abspath(path)

    files = get_git_files(path)
    tree = build_tree(files)
    print('.')
    print_tree(tree)

if __name__ == '__main__':
    main()
