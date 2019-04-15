# BlogGen - A simple static blog generator

Bloggen is a simple static blog generator written in Python.

## Usage

1. Clone this repository
1. Run `pip install -r requirements.txt` (You may want to create
   a [virtualenv][virtualenv] first)
1. Run the `generate.py` script.

`generate.py` looks for Markdown files in the `posts` directory and
converts them to a set of HTML files in the `site` directory. It will
also generate an index page at `site/index.html`

Once generated, the `site` directory can be served with any regular
webserver, e.g.

    cd site && python -m http.server 8080

If you want to include static assets (images, CSS, JavaScript, etc),
put them in the `static` directory. The `generate.py` script will copy
the contents of this directory to `site/static/`.

## Markdown

Bloggen uses [Python-Markdown][pymark] for converting Markdown
documents to HTML and its [Meta-Data extension][metadata] extension
for blog post metadata. At a minimum, each blog entry needs to have
the `Title` and `Date` fields set.

[pymark]: https://python-markdown.github.io
[metadata]: https://python-markdown.github.io/extensions/meta_data/
[virtualenv]: https://virtualenv.pypa.io/
