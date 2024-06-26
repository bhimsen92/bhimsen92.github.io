import markdown2
from jinja2 import Environment, FileSystemLoader
import frontmatter
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
import os
import click


TEMPLATE_FOLDER = "templates"
POSTS_FOLDER = "posts"


class HighlightRenderer(markdown2.Markdown):
    def _code(self, code, language):
        lexer = get_lexer_by_name(language, stripall=True)
        formatter = HtmlFormatter()
        return highlight(code, lexer, formatter)


def main():
    jinja_env = Environment(loader=FileSystemLoader(TEMPLATE_FOLDER))
    markdown_files = list_files_sorted_by_creation_time(TEMPLATE_FOLDER)
    
    renderer = HighlightRenderer(extras=["fenced-code-blocks"])

    post_titles = []
    for markdown_file in markdown_files:
        file_path = os.path.join(TEMPLATE_FOLDER, markdown_file)        
        with open(file_path, 'r') as file:
            post = frontmatter.load(file)

        if len(post.content.strip()) == 0:
            continue

        html_content = renderer.convert(post.content)

        template = jinja_env.get_template("layout.jinja")
        rendered_html = template.render(
            title=post.metadata['title'],
            date=post.metadata['date'],
            tags=post.metadata['tags'],
            content=html_content
        )

        output_file = f"{markdown_file.split('.')[0]}.html"
        output_path = os.path.join(POSTS_FOLDER, output_file)
        with open(output_path, "w") as f:
            f.write(rendered_html)

        if markdown_file != "about.md":
            post_titles.append((post["title"], output_file))
        
        click.echo(f"Rendered {markdown_file} to {output_file}")



    template = jinja_env.get_template("index.jinja")
    rendered_template = template.render(post_titles=post_titles)

    with open("index.html", "w") as f:
        f.write(rendered_template)
    click.echo(f"Rendered index.jinja to index.html")


def list_files_sorted_by_creation_time(directory):
    return sorted(
        [
            file
            for file in os.listdir(directory) if file.endswith(".md")
        ],
        key=lambda x: os.stat(os.path.join(directory, x)).st_ctime,
        reverse=True,
    )


if __name__ == "__main__":
    main()
