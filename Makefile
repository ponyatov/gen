MODULE = $(notdir $(CURDIR))

PY = $(shell which python3)

all: $(PY) $(MODULE).py
	$^
