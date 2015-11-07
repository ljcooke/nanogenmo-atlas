.PHONY: all story bootstrap stats clean

all: bootstrap story

story:
	./atlas.py generate

bootstrap:
	./bootstrap.sh

stats:
	./atlas.py stats

clean:
	rm -rf data
