from shutil import rmtree, copy
import os


def move_generated_content(from_path: str, to_path: str):
    if not os.path.exists(to_path):
        os.makedirs(to_path)
    for entry in os.listdir(from_path):
        src = os.path.join(from_path, entry)
        dst = os.path.join(to_path, entry)
        if os.path.isdir(src):
            move_generated_content(src, dst)
        else:
            copy(src, dst)
