# \ <section:var>
MODULE   = $(notdir $(CURDIR))
NOW      = $(shell date +%d%m%y)
REL      = $(shell git rev-parse --short=4 HEAD)
# / <section:var>

# \ <section:tool>
WGET     = wget -c
PY       = $(shell which python3)
# / <section:tool>

all: $(PY) $(MODULE).py
	$^ $@

MERGE  = Makefile LICENSE README.md .gitignore .vscode
MERGE += $(MODULE).py

main:
	git checkout $@
	git checkout shadow -- $(MERGE)

shadow:
	git checkout $@

release:
	git tag $(NOW)-$(REL)
	git push -v && git push -v --tags
	$(MAKE) shadow
