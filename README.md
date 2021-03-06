# Bloggen - A simple static blog generator

Bloggen is a simple static blog generator written in Python.

## Usage

1. Fork and / or clone this repository
1. Make sure you have Python 3.7 (or later) installed. You may also
   want to create a [virtualenv][virtualenv] for this project.
1. Run `pip install -r requirements.txt`
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

## Hacking

Bloggen uses [pip-tools][pip-tools] for managing dependencies, so if you want
to customize Bloggen (which I highly encourage!) you'll need to install it:

```sh
# inside your virtual env:
pip install pip-tools
```

To install regular and development dependencies, do:

```sh
pip-sync requirements.txt dev-requirements.txt
```

## Markdown

Bloggen uses [Python-Markdown][pymark] for converting Markdown
documents to HTML and its [Meta-Data extension][metadata] extension
for blog post metadata.

At a minimum, each blog entry needs to have the `Title` and `Date`
fields set.

## Netlify

Blogs made with Bloggen are ready to be deployed to Netlify. Check out
Netlify's [Continuous Deployment][deployment] documentation for
further instructions.

[pymark]: https://python-markdown.github.io
[metadata]: https://python-markdown.github.io/extensions/meta_data/
[virtualenv]: https://virtualenv.pypa.io/
[deployment]: https://www.netlify.com/docs/continuous-deployment/
[pip-tools]: https://github.com/jazzband/pip-tools
