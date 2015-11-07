.PHONY: all story bootstrap clean

all: bootstrap story

story:
	./atlas.py generate

bootstrap:
	./bootstrap.sh

clean:
	rm -rf data
