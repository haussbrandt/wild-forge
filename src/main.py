import os
import shutil
import sys

from convert import markdown_to_html_node

def copy_static_to_docs():
    try:
        shutil.rmtree("docs")
    except FileNotFoundError:
        pass

    for path in os.walk("static"):
        old_path = path[0]
        new_path = "docs/" + "/".join(path[0].split("/")[1:])
        # print(new_path)
        os.mkdir(new_path)
        for file in path[2]:
            # print(f'{old_path + "/" + file} -> {new_path + "/" + file}')
            shutil.copy(old_path + "/" + file, new_path + "/" + file)

def extract_title(markdown):
    first_line = markdown.split("\n")[0]
    if first_line.startswith("# "):
        return first_line[2:]
    else:
        raise ValueError("Title heading is missing")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} for {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        content = f.read()
    with open(template_path, "r") as f:
        template = f.read()

    html = markdown_to_html_node(content).to_html()
    title = extract_title(content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')

    with open(dest_path, "w+") as f:
        f.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath): 
    for path in os.walk(dir_path_content):
        old_path = path[0]
        new_path = dest_dir_path + "/".join(path[0].split("/")[1:])
        # print(new_path)
        try:
            os.mkdir(new_path + "/")
        except FileExistsError:
            pass
        for file in path[2]:
            if not file.endswith(".md"):
                continue
            # print(f'{old_path + "/" + file} -> {new_path + "/" + file}')
            generate_page(old_path + "/" + file, template_path, new_path + "/" + file[:-3] + ".html", basepath)

if __name__ == "__main__":
    basepath = sys.argv[1] if len(sys.argv) >= 2 else "/"
    copy_static_to_docs()
    generate_pages_recursive("content", "template.html", "docs/", basepath)