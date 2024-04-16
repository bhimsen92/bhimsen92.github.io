import re
import os
import click
from jinja2 import Environment, FileSystemLoader
from jinja2.ext import Extension
from jinja2 import nodes
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter


TEMPLATE_FOLDER = "templates"
POSTS_FOLDER = "posts"


class CodeBlockExtension(Extension):
    tags = {"code"}

    HTML_START = """
    <div class="container mx-auto my-4">
    <div class="bg-white rounded-lg shadow-md border border-gray-300">
        <pre class="rounded-lg overflow-x-auto"><code class="block p-2 text-sm text-gray-900 {}">
        """

    HTML_END = """</code></pre></div></div>"""

    def parse(self, parser):
        lineno = next(parser.stream).lineno

        args = []
        if parser.stream.current.type == "string":
            args = [parser.parse_expression()]
        else:
            args = [nodes.Const(None)]

        body = parser.parse_statements(["name:endcode"], drop_needle=True)
    
        rendered_block = nodes.CallBlock(
            self.call_method("_render_block", args), [], [], body
        ).set_lineno(lineno)

        return rendered_block

    def _render_block(self, language, caller):
        if not language:
            language = ''

        return self.HTML_START.format(language) + caller() + self.HTML_END


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
    jinja_env.add_extension(CodeBlockExtension)

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
