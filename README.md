# BlogGen - A simple static blog generator

Bloggen is a simple static blog generator written in Python. It takes
the contents of the `posts` directory and tries to convert it to
a set of HTML files in the `site` directory.

From there you can serve the site, e.g. with:

    python -m http.server 8080

## Markdown

Bloggen uses [Python-Markdown][pymark] for converting Markdown
documents to HTML.

Pay special attention to the documentation for the [Meta-Data
extension][metadata] extension.

[pymark]: https://python-markdown.github.io
[metadata]: https://python-markdown.github.io/extensions/meta_data/
