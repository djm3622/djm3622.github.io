.PHONY: build thumbnails test check

build:
	bundle exec jekyll build

thumbnails:
	python3 scripts/build_publication_thumbnails.py

test:
	python3 -m unittest discover -s tests -p 'test_*.py'

check: test build
