import re
import os
import click
from jinja2 import Environment, FileSystemLoader
from jinja2.ext import Extension
from jinja2 import nodes
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

from extensions import MarkdownExtension


TEMPLATE_FOLDER = "templates"
POSTS_FOLDER = "posts"


def to_blog_title(value):
    value_without_extension = os.path.splitext(value)[0]
    return " ".join(
        [w.capitalize() for w in re.split(r"[-_]", value_without_extension)]
    )


def to_html_extension(value):
    return value.replace(".jinja", ".html")


def list_files_sorted_by_creation_time(directory):
    return sorted(
        [
            file
            for file in os.listdir(directory)
            if file.endswith(".jinja") and file not in ["base.jinja", "layout.jinja"]
        ],
        key=lambda x: os.stat(os.path.join(directory, x)).st_ctime,
    )


@click.command()
def render_templates():
    os.makedirs(POSTS_FOLDER, exist_ok=True)

    jinja_env = Environment(loader=FileSystemLoader(TEMPLATE_FOLDER))
    jinja_env.filters["to_blog_title"] = to_blog_title
    jinja_env.filters["to_html_extension"] = to_html_extension
    
    jinja_env.add_extension(MarkdownExtension)

    template_files = list_files_sorted_by_creation_time(TEMPLATE_FOLDER)

    for template_file in template_files:
        template = jinja_env.get_template(template_file)
        rendered_template = template.render(
            template_files=template_files, skip_files=["about.jinja", "index.jinja"]
        )

        output_file = os.path.join(POSTS_FOLDER, f"{template_file.split('.')[0]}.html")

        with open(output_file, "w") as f:
            f.write(rendered_template)

        click.echo(f"Rendered {template_file} to {output_file}")


if __name__ == "__main__":
    render_templates()
