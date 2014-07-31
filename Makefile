
export PYTHONPATH=.

name=$(shell grep Name: bento.info | awk '{print $$NF}')
version=$(shell grep Version: bento.info | awk '{print $$NF}')
distfile=dist/$(name)-$(version).tar.gz	

all: lint test

docs: build_docs

build_docs:
	cd docs && make html
	pandoc -t rst README.md | sed -e '1,1s/^[^\\]*//' -e '2d' > README.rst

lint:
	pylint jwt test bench

test: run_test

run_test:
	./test/run/run_pyvows.py -v test

coverage: run_coverage

run_coverage:
	./test/run/run_pyvows.py -v --cover --cover-package jwt --cover-report coverage/coverage.xml test

bench: run_bench

run_bench:
	for b in ./bench/*_bench.py; do $$b; done

bench_gfm: 
	for b in ./bench/*_bench.py; do $$b --gfm; done

node_deps:
	mkdir -p node_modules && npm install jsjws sinon

dist: make_dist

make_dist:
	rm -f $(distfile)
	./dist/bentomaker.py --build-directory=dist/build \
                             sdist \
                             --output-dir=dist

travis_test: lint
	./test/run/run_coverage.py run --source=jwt -m test.run.run_pyvows -v test

register:
	./dist/bentomaker.py --build-directory=dist/build register_pypi

upload:
	./dist/bentomaker.py --build-directory=dist/build upload_pypi -t source $(distfile)
