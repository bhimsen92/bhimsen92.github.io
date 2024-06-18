SHELL := /bin/zsh

.PHONY: render_templates build_css format_html

all: render_templates build_css

render_templates:
	python ./render_templates.py

build_css:
	npm run build:css

format_html:
	npm run format:html
