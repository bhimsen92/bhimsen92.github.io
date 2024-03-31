import re
import os
import click
from jinja2 import Environment, FileSystemLoader
from jinja2.ext import Extension
from jinja2 import nodes


TEMPLATE_FOLDER = "templates"
POSTS_FOLDER = "posts"


class CodeBlockExtension(Extension):
    tags = {'code'}
    
    HTML_START = """
    <!-- prettier-ignore-start -->
    <div class="container mx-auto py-8">
    <div class="bg-white rounded-lg shadow-md">
        <pre class="p-2 rounded-lg overflow-x-auto">
            <code class="block p-4 text-sm text-gray-800">
    """
    HTML_END = """
        </code></pre></div></div>
        <!-- prettier-ignore-end -->
    """
    
    def parse(self, parser):
        lineno = next(parser.stream).lineno
        body = parser.parse_statements(['name:endcode'], drop_needle=True)
        return nodes.CallBlock(self.call_method('_render_block', []),
                               [], [], body).set_lineno(lineno)

    def _render_block(self, caller):
        return self.HTML_START + caller() + self.HTML_END


def to_blog_title(value):
    value_without_extension = os.path.splitext(value)[0]
    return " ".join([w.capitalize() for w in re.split(r'[-_]', value_without_extension)])


def to_html_extension(value):
    return value.replace(".jinja", ".html")


@click.command()
def render_templates():
    os.makedirs(POSTS_FOLDER, exist_ok=True)

    jinja_env = Environment(loader=FileSystemLoader(TEMPLATE_FOLDER))
    jinja_env.filters['to_blog_title'] = to_blog_title
    jinja_env.filters['to_html_extension'] = to_html_extension
    jinja_env.add_extension(CodeBlockExtension)

    template_files = [
        f for f in os.listdir(TEMPLATE_FOLDER) if f.endswith(".jinja") and f not in ["base.jinja", "layout.jinja"]
    ]

    for template_file in template_files:
        template = jinja_env.get_template(template_file)
        rendered_template = template.render(template_files=template_files, skip_files=["about.jinja", "index.jinja"])

        output_file = os.path.join(POSTS_FOLDER, f"{template_file.split('.')[0]}.html")

        with open(output_file, "w") as f:
            f.write(rendered_template)
        
        click.echo(f"Rendered {template_file} to {output_file}")


if __name__ == "__main__":
    render_templates()

