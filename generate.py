#!/usr/bin/env python
import os
from jinja2 import Environment, FileSystemLoader, Markup, select_autoescape
import markdown

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
env = Environment(
    loader=FileSystemLoader(os.path.join(BASE_DIR, 'templates')),
    autoescape=select_autoescape(['html', 'xml'])
)

try:
    os.makedirs(os.path.join(BASE_DIR, 'site'))
except FileExistsError:
    pass

for post in os.listdir(os.path.join(BASE_DIR, 'posts')):
    with open(os.path.join(BASE_DIR, 'posts', post), 'r') as f:
        post_html = markdown.markdown(f.read())
    template = env.get_template('post.html')
    html = template.render(
        post_html=Markup(post_html)
    )
    filename = os.path.join(
        BASE_DIR,
        'site',
        os.path.splitext(os.path.basename(post))[0]
    )
    with open(filename, 'w') as f:
        f.write(html)
