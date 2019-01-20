
.PHONY: init test

test:
	py.test tests

init:
	pip3 install -e .
