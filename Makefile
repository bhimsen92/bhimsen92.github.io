SHELL := /bin/zsh

.PHONY: markdown_to_html build_css format_html

all: markdown_to_html build_css format_html

markdown_to_html:
	python ./markdown_to_html.py

build_css:
	npm run build:css

format_html:
	npm run format:html
