PATH := $(PWD)/.venv/bin:$(shell printenv PATH)
SHELL := env PATH=$(PATH) /bin/bash
VENV_DIR=.venv

## Destroy docker instances, remove virtualenv, molecule temp, .pyc files
.PHONY: clean
clean:
	rm -rf .venv

## Create virtualenv, install dependencies
deps:
	test -d ${VENV_DIR} || virtualenv ${VENV_DIR}
	${VENV_DIR}/bin/pip install -r requirements/main.txt
	virtualenv --relocatable ${VENV_DIR}
	python setup.py install

.PHONY: help
help:
	@awk -v skip=1 \
		'/^##/ { sub(/^[#[:blank:]]*/, "", $$0); doc_h=$$0; doc=""; skip=0; next } \
		 skip  { next } \
		 /^#/  { doc=doc "\n" substr($$0, 2); next } \
		 /:/   { sub(/:.*/, "", $$0); \
		 printf "\033[34m%-30s\033[0m\033[1m%s\033[0m %s\n\n", $$0, doc_h, doc; skip=1 }' \
		$(MAKEFILE_LIST)

## Run tests
test: deps
	python setup.py nosetests
