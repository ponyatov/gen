MODULE = $(notdir $(CURDIR))

PY = $(shell which python3)

all: $(PY) $(MODULE).py
	$^

MERGE  = Makefile LICENSE README.md .gitignore .vscode
MERGE += $(MODULE).py

main:
	git checkout $@
	git checkout shadow -- $(MERGE)

shadow:
	git checkout $@
