.PHONY: build test check

build:
	bundle exec jekyll build

test:
	python3 -m unittest discover -s tests -p 'test_*.py'

check: test build
