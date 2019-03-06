
.PHONY: init test

test:
	py.test tests

run:
	python3 -m lexicamaker ${ARGS}

init:
	pip3 install -e .
