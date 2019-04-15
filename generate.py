#!/usr/bin/env python
import os
import shutil

import toml
from jinja2 import Environment, FileSystemLoader, Markup, select_autoescape
import markdown

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SITE_PATH = os.path.join(BASE_DIR, "site")
CONFIG_FILE = "config.toml"

env = Environment(
    loader=FileSystemLoader(os.path.join(BASE_DIR, "templates")),
    autoescape=select_autoescape(["html", "xml"]),
)

try:
    os.makedirs(SITE_PATH)
except FileExistsError:
    pass


def load_config():
    return toml.load(CONFIG_FILE)


def generate_posts():
    metadata = []
    for post in os.listdir(os.path.join(BASE_DIR, "posts")):
        md = markdown.Markdown(
            extensions=["meta", "fenced_code", "codehilite", "smarty"]
        )
        with open(os.path.join(BASE_DIR, "posts", post), "r") as f:
            post_html = md.convert(f.read())
        template = env.get_template("post.html")
        html = template.render(
            title=md.Meta["title"][0],
            post_html=Markup(post_html),
            author=", ".join(md.Meta["authors"])
        )
        filename = os.path.splitext(os.path.basename(post))[0] + ".html"
        md.Meta["filename"] = filename
        metadata.append(md.Meta)
        path = os.path.join(SITE_PATH, filename)
        with open(path, "w") as f:
            f.write(html)
    return metadata


def generate_index_page(posts_metadata):
    config = load_config()
    posts_metadata.sort(key=lambda x: x["date"][0])
    index_template = env.get_template("index.html")
    html = index_template.render(title=config["title"], posts=posts_metadata)
    filename = os.path.join(SITE_PATH, "index.html")
    with open(filename, "w") as f:
        f.write(html)


def copy_static_files():
    static_src_path = os.path.join(BASE_DIR, "static")
    static_dest_path = os.path.join(SITE_PATH, "static")
    try:
        shutil.rmtree(static_dest_path)
    except FileNotFoundError:
        pass
    shutil.copytree(static_src_path, static_dest_path)


if __name__ == "__main__":
    print("Generating posts...")
    posts_metadata = generate_posts()
    print("Generating index page...")
    generate_index_page(posts_metadata)
    print("Copying static files...")
    copy_static_files()
