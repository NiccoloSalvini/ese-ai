.PHONY: preview build deploy clean

preview:        ## live reload while editing
	quarto preview

build:          ## render -> _site/
	quarto render

deploy: build   ## render locally, push _site/ to the gh-pages branch
	quarto publish gh-pages --no-render --no-prompt

clean:
	rm -rf _site .quarto
