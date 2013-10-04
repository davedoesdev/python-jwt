
export PYTHONPATH=.

name=$(shell grep Name: bento.info | awk '{print $$NF}')
version=$(shell grep Version: bento.info | awk '{print $$NF}')

all: lint test

docs: build_docs

build_docs:
	cd docs && make html
	pandoc -t rst README.md | sed -e '1,1s/^[^\\]*//' -e '2d' > README.rst

lint:
	pylint jwt test bench

test: run_test

run_test:
	./test/run/run_pyvows.py test

coverage: run_coverage

run_coverage:
	./test/run/run_pyvows.py --cover --cover-package jwt --cover-report coverage/coverage.xml test

bench: run_bench

run_bench:
	for b in ./bench/*_bench.py; do $$b; done

bench_gfm: 
	for b in ./bench/*_bench.py; do $$b --gfm; done

node_deps:
	mkdir -p node_modules && npm install jsjws sinon

dist: make_dist

make_dist:
	rm -f dist/$(name)-$(version).tar.gz	
	./dist/bentomaker.py --build-directory=dist/build \
                             sdist \
                             --output-dir=dist
	gunzip dist/$(name)-$(version).tar.gz
	tar --transform='s,^dist/,$(name)-$(version)/,' -rf dist/$(name)-$(version).tar dist/setup.py dist/bentomaker.py dist/dependency_links.txt
	tar --transform='s,^,$(name)-$(version)/,' -rf dist/$(name)-$(version).tar README.rst
	gzip dist/$(name)-$(version).tar

travis_test: lint
	./test/run/run_coverage.py run --source=jwt -m test.run.run_pyvows test

register:
	./dist/bentomaker.py --build-directory=dist/build register_pypi

upload:
	./dist/bentomaker.py --build-directory=dist/build upload_pypi -t source dist/$(name)-$(version).tar.gz
