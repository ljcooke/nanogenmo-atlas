.PHONY: all bootstrap clean

all:
	./atlas.py generate

bootstrap:
	./bootstrap.sh

clean:
	rm -rf data
