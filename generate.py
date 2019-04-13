#!/usr/bin/env python
import timeit
import os
import shutil
from jinja2 import Environment, FileSystemLoader, Markup, select_autoescape
import markdown

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SITE_PATH = os.path.join(BASE_DIR, 'site')

env = Environment(
    loader=FileSystemLoader(os.path.join(BASE_DIR, 'templates')),
    autoescape=select_autoescape(['html', 'xml'])
)

try:
    os.makedirs(SITE_PATH)
except FileExistsError:
    pass


def generate_posts():
    metadata = []
    for post in os.listdir(os.path.join(BASE_DIR, 'posts')):
        md = markdown.Markdown(extensions=['meta'])
        with open(os.path.join(BASE_DIR, 'posts', post), 'r') as f:
            post_html = md.convert(f.read())
        metadata.append(md.Meta)
        template = env.get_template('post.html')
        html = template.render(
            post_html=Markup(post_html)
        )
        filename = os.path.join(
            SITE_PATH,
            os.path.splitext(os.path.basename(post))[0]
        )
        with open(filename, 'w') as f:
            f.write(html)
    return metadata

def generate_index_page(posts_metadata):
    index_template = env.get_template('index.html')
    html = index_template.render(posts=posts_metadata)
    filename = os.path.join(SITE_PATH, 'index.html')
    with open(filename, 'w') as f:
        f.write(html)

def copy_static_files():
    static_src_path = os.path.join(BASE_PATH, 'static')
    static_dest_path = os.path.join(SITE_PATH, 'static')
    shutil.rmtree(static_dest_path)
    shutil.copytree(static_src_path, static_dest_path)

if __name__ == '__main__':
    print('Generating posts...')
    posts_metadata = generate_posts()
    print('Generating index page...')
    generate_index_page(posts_metadata)
    print('Copying static files...')
    copy_static_files()
