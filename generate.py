#!/usr/bin/env python
import datetime
import os
import urllib
import shutil
from collections import namedtuple

import toml
from jinja2 import Environment, FileSystemLoader, Markup, select_autoescape
import markdown

Post = namedtuple("Post", ["html", "meta"])

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SITE_PATH = os.path.join(BASE_DIR, "site")
CONFIG_FILE = "config.toml"
FEED_FILENAME = "feed.rss"

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


def generate_posts(posts):
    for post in posts:
        template = env.get_template("post.html")
        html = template.render(
            title=post.meta["title"][0],
            date=post.meta["date"][0],
            post_html=Markup(post.html),
            description=" ".join(post.meta["description"]),
            authors=", ".join(post.meta["authors"]),
        )
        path = os.path.join(SITE_PATH, post.meta["filename"])
        with open(path, "w") as f:
            f.write(html)


def generate_index_page(config, posts):
    posts_metadata = [p.meta for p in posts]
    template = env.get_template("index.html")
    html = template.render(
        feed_url=feed_url(config),
        title=config["title"],
        description=config["description"],
        posts=posts_metadata,
    )
    filename = os.path.join(SITE_PATH, "index.html")
    with open(filename, "w") as f:
        f.write(html)


def generate_feed(config, posts):
    template = env.get_template("feed.rss")
    xml = template.render(
        config=config,
        posts=posts,
        self_url=feed_url(config),
        last_pub_date=posts[0].meta["iso_date"],
    )
    filename = os.path.join(SITE_PATH, FEED_FILENAME)
    with open(filename, "w") as f:
        f.write(xml)


def feed_url(config):
    return urllib.parse.urljoin(config["url"], "feed.rss")


def copy_static_files():
    static_src_path = os.path.join(BASE_DIR, "static")
    static_dest_path = os.path.join(SITE_PATH, "static")
    try:
        shutil.rmtree(static_dest_path)
    except FileNotFoundError:
        pass
    shutil.copytree(static_src_path, static_dest_path)


def parse_markdown(config):
    for post in os.listdir(os.path.join(BASE_DIR, "posts")):
        md = markdown.Markdown(
            extensions=["meta", "fenced_code", "codehilite", "smarty"]
        )
        with open(os.path.join(BASE_DIR, "posts", post), "r") as f:
            post_html = md.convert(f.read())
        filename = os.path.splitext(os.path.basename(post))[0] + ".html"
        md.Meta["filename"] = filename
        md.Meta["url"] = urllib.parse.urljoin(config["url"], filename)
        md.Meta["iso_date"] = to_rfc_3339(md.Meta["date"][0])
        yield Post(meta=md.Meta, html=post_html)


def to_rfc_3339(iso_datetime):
    dt = datetime.datetime.fromisoformat(iso_datetime)
    return dt.isoformat("T") + "Z"


def to_canonical_url(url):
    return url + "/" if url[-1] != "/" else ""


if __name__ == "__main__":
    print("Loading configuration")
    config = load_config()
    print("Generating posts...")
    posts = list(parse_markdown(config))
    posts.sort(key=lambda x: x.meta["date"][0])
    generate_posts(posts)
    print("Generating index page...")
    generate_index_page(config, posts)
    generate_feed(config, posts)
    print("Copying static files...")
    copy_static_files()
