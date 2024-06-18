from jinja2 import nodes
from jinja2.ext import Extension


class MarkdownExtension(Extension):
    tags = {
        'header', 'date', 'figure', 'link', 'p', 'bold', 'italic', 'ordered_list', 
        'unordered_list', 'code_block', 'container', 'row', 'column', 'item',
        'new_line', "space",
    }

    def parse(self, parser):
        tag = next(parser.stream)
        lineno = tag.lineno
        kwargs = []

        while parser.stream.current.type != "block_end":
            key = parser.parse_assign_target()
            parser.stream.expect("assign")
            value = parser.parse_expression()

            kwargs.append(nodes.Keyword(key.name, value))
        
        if tag.value not in ['new_line', 'space']:
            body = parser.parse_statements(['name:end' + tag.value], drop_needle=True)
        else:
            body = ""
    
        return nodes.CallBlock(
            self.call_method(tag.value, [], kwargs), [], [], body
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
    def p(self, caller):
        content = caller()
        return f"""
            <p class="my-4 text-lg">{content}</p>
        """
    
    def bold(self, caller):
        return f"""
            <strong class="font-bold">{caller()}</strong>
        """
    
    def italic(self, caller):
        return f"""
            <em class="italic">{caller()}</em>
        """
    
    def ordered_list(self, caller):
        items = caller().strip().split("\n")
        list_items = ''.join([f'<li class="mb-2">{item}</li>' for item in items])
        return f"""
            <ol class="list-decimal list-inside my-4>{list_items}</ol>"
        """
    
    def unordered_list(self, caller):
        items = caller().strip().split("\n")
        list_items = ''.join([f'<li class="mb-2">{item}</li>' for item in items])
        return f"""
            <ul class="list-disc list-inside my-4>{list_items}</ul>"
        """
    
    def code_block(self, caller, language):
        content = caller().strip()
        html = f"""<pre class="bg-gray-100 rounded p-4 overflow-auto"><code class="{language}">{content}</code></pre>"""

        return html
    
    def container(self, caller, type="flex", direction="row", wrap="wrap", justify="start", align="strech"):
        content = caller()
        if type == "flex":
            html = f"""
                <div class="flex flex-{direction} flex-{wrap} justify-{justify} items-{align}">{content}</div>
            """
        elif type == "grid":
            html = f"""
                <div class="grid grid-cols-{direction}">{content}</div>
            """
        else:
            html = content
        
        return html

    def row(self, caller):
        return f"""<div class="flex flex-row">{caller()}</div>"""
    
    def column(self, caller):
        return f"""<div class="flex-1">{caller()}</div>"""
    
    def item(self, caller):
        return f"""<div class="p-4">{caller()}</div>"""

    def new_line(self, caller, count=2):
        return "<br>" * count
    
    def space(self, caller, count=1):
        return "&nbsp;" * count