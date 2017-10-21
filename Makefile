PYTHON:="$(shell which python3)"
VENV_DIR=.venv
pip_install:=$(VENV_DIR)/bin/pip install -r


.PHONY: build
build: $(VENV_DIR)

$(VENV_DIR):
	$(PYTHON) -m venv --copies $(VENV_DIR)
	$(pip_install) requirements.txt


.PHONY: clean
clean:
	rm -rf $(VENV_DIR)
