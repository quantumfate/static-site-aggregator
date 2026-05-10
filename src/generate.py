from ntpath import isdir
from pathlib import Path
from shutil import rmtree, copy
import shutil
from markdown_convert import markdown_to_html_node
import os


def move_generated_content(from_path: str, to_path: str, recursion_level: int = 0):
    if recursion_level == 0 and os.path.exists(to_path):
        shutil.rmtree(to_path)
    if not os.path.exists(to_path):
        os.makedirs(to_path)
    for entry in os.listdir(from_path):
        src = os.path.join(from_path, entry)
        dst = os.path.join(to_path, entry)
        if os.path.isdir(src):
            move_generated_content(src, dst, recursion_level + 1)
        else:
            copy(src, dst)


def extract_title(markdown: str) -> str:
    if markdown.startswith("# "):
        return markdown.split("\n")[0].split(maxsplit=1)[1]
    raise ValueError("Not a valid markdown h1")


def generate_page(from_path: str, dest_path: str, template_path: str, basepath: str):
    print(f"Generating page {from_path} to {dest_path} using {template_path}")
    md_f = open(from_path, "r")
    html_template_f = open(template_path, "r")

    md_file_content = md_f.read()
    html_template = html_template_f.read()

    converted_html = markdown_to_html_node(md_file_content).to_html()
    md_title = extract_title(md_file_content)
    html_template = html_template.replace("{{ Title }}", md_title)
    html_template = html_template.replace("{{ Content }}", converted_html)
    html_template = html_template.replace('href="/', f'href="{basepath}')
    html_template = html_template.replace('src="/', f'src="{basepath}')
    md_f.close()

    working_dir_abs = os.path.abspath(dest_path)
    target_dir, _ = os.path.split(working_dir_abs)
    os.makedirs(target_dir, exist_ok=True)
    dest_f = open(dest_path, "w")
    dest_f.write(html_template)
    dest_f.close()
    html_template_f.close()


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str
):
    for entry in os.listdir(dir_path_content):
        src = os.path.join(dir_path_content, entry)
        dst = os.path.join(dest_dir_path, entry)
        if os.path.isdir(src):
            generate_pages_recursive(src, template_path, dst, basepath)
        else:
            generate_page(src, dst.split(".")[0] + ".html", template_path, basepath)
