all: bootstrap

bootstrap:
	./bootstrap.sh

clean:
	(cd corpus/OpenExoplanetCatalogue && rm -f ./*.xml ./*.xml~)
