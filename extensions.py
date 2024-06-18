from jinja2 import nodes
from jinja2.ext import Extension


class MarkdownExtension(Extension):
    tags = {
        'header', 'date', 'figure', 'link', 'paragraph', 'bold', 'italic', 'ordered_list', 
        'unordered_list', 'code_block', 'container', 'row', 'column', 'item',
    }

    def parse(self, parser):
        tag = next(parser.stream)
        lineno = tag.lineno
        args = []
        kwargs = []

        while parser.stream.current.type != "block_end":
            key = parser.parse_assign_target()
            parser.stream.expect("assign")
            value = parser.parse_expression()

            kwargs.append(nodes.Keyword(key, value))
        
        body = parser.parse_statements(['name:end' + tag.value], drop_needle=True)
        return nodes.CallBlock(
            self.call_method(tag.value, args, kwargs), [], [], body
        ).set_lineno(lineno)
    
    def header(self, caller, level="medium"):
        levels = {
            "extra-large": ("h1", "5xl"),
            "large": ("h2", "4xl"),
            "medium": ("h3", "3xl"),
            "small": ("h4", "2xl"),
            "extra-small": ("h5", "xl")
        }

        tag, style = levels[level]
        content = f"""
            <{tag} class="{style} font-bold my-4">{caller()}</{tag}>
        """

        return content

    def date(self, caller):
        return f"""<time class="text-sm text-gray-500">{caller()}</time>"""
    
    def figure(self, caller, src, alt=""):
        return f'''<figure class="my-4"><img src="{src}" alt="{alt}" class="rounded shadow"/><figcaption class="text-center text-sm text-gray-500 mt-2">{alt}</figcaption></figure>'''

    def link(self, caller, href):
        link_text = caller()
        return f"""
            <a href={href} class="text-blue-500 hover:text-blue-700 underline">{link_text}</a>
        """
    
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

