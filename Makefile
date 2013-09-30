
export PYTHONPATH=.
PYVOWS = ./test/pyvows.sh

all: lint test

docs: build_docs

build_docs:
	cd docs && make html

lint:
	pylint jwt test bench

test: run_test

run_test:
	$(PYVOWS) test

coverage: run_coverage

run_coverage:
	$(PYVOWS) --cover --cover-package jwt --cover-report coverage/coverage.xml test

bench: run_bench

run_bench:
	for b in ./bench/*_bench.py; do $$b; done

bench_gfm: 
	for b in ./bench/*_bench.py; do $$b --gfm; done

dev_deps:
	mkdir -p node_modules && npm install jsjws sinon
