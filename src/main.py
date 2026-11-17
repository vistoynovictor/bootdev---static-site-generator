from os import path, listdir, mkdir, makedirs
from shutil import rmtree, copy
import re
from translator import markdown_to_html_node
from sys import argv


def main(basepath: str = "/"):
    if argv[1] and type(argv[1] == str):
        basepath = argv[1]

    set_files("docs/", "static/")
    generate_pages_recursive("content/", "template.html", "docs/", basepath)


def set_files(target_path: str, origin_path: str):
    target = path.abspath(target_path)
    origin = path.abspath(origin_path)
    if path.exists(target):
        print(f"Old target: {listdir(target)}")
        rmtree(target)
        print(f"Removed old target dir {target}")
    mkdir(target)
    print(f"Created target dir {target}")

    if path.exists(origin):
        list = listdir(origin)
        for item in list:
            current_origin_path = path.join(origin, item)
            current_target_path = path.join(target, item)
            print(f"""
Intended Origin Path: {current_origin_path}
Intended Target path: {current_target_path}
            """)
            if path.isfile(current_origin_path):
                print(f"Copied {current_origin_path} to {current_target_path}")
                copy(current_origin_path, current_target_path)
            else:
                mkdir(current_target_path)
                print(f"Created dir {current_target_path}")
                print("🔻🔻- Going Down the path -🔻🔻")
                set_files(current_target_path, current_origin_path)
    else:
        raise Exception(f"Nothing to convert in dir {origin_path}")


def extract_title(markdown: str):
    match = re.compile(r"\# (\w+[\w\s,;&$\(\)\[\]\"\'`\-_*]*)")
    h1 = match.findall(markdown)
    if len(h1) == 0:
        raise Exception("No header of level 1 found in markdown text provided")
    heading = h1[0].strip()
    return heading


def generate_page(from_path, template_path, dest_path, basepath: str):
    from_path = path.abspath(from_path)
    template_path = path.abspath(template_path)
    dest_path = path.abspath(dest_path)

    if not path.isfile(from_path):
        raise Exception(f"Path {from_path} is not a valid path")

    if not path.isfile(template_path):
        raise Exception(f"Path {template_path} is not a valid path")

    slash_index = len(dest_path) - 1
    for i in range(len(dest_path) - 1, -1, -1):
        if dest_path[i] == "/":
            slash_index = i + 1
            break
    dest_dir = dest_path[:slash_index]
    if not path.exists(dest_dir):
        makedirs(dest_dir)

    print(f"\nGeneration from {from_path} to {dest_path} using {template_path}")

    markdown: str
    with open(from_path, encoding="utf-8") as f:
        markdown = f.read()

    template: str
    with open(template_path, encoding="utf-8") as f:
        template = f.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    insertable_values: list[str] = [title, html]

    match_placeholders = re.compile(r"\{\{ \w+ \}\}")
    splitted_template = match_placeholders.split(template)
    template_list: list[str] = []
    for i in range(len(splitted_template)):
        template_list.append(splitted_template[i])
        if i < len(insertable_values):
            template_list.append(insertable_values[i])
    template_filled = "".join(template_list)

    template_linked = re.sub(r'href="/', f'href="{basepath}', template_filled)
    template_sourced = re.sub(r'src="/', f'src="{basepath}', template_linked)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(template_sourced)


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str
):
    content = path.abspath(dir_path_content)
    if dest_dir_path.endswith("/"):
        dest_dir_path = dest_dir_path[:-1]

    if not path.isdir(content):
        raise Exception(f"Path {content} is not a directory")

    for entry in listdir(content):
        entry_path = f"{content}/{entry}"
        new_dest = f"{dest_dir_path}/{entry}"
        print(f"👉 entry: {entry_path}, dest: {new_dest}")

        if path.isfile(entry_path) and entry_path.endswith(".md"):
            file_name = new_dest[:-3]
            generate_page(entry_path, template_path, file_name + ".html", basepath)
        if path.isdir(entry_path):
            generate_pages_recursive(entry_path, template_path, new_dest, basepath)


if __name__ == "__main__":
    main()
