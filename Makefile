init:
	pip install -r requirements.txt

init-dev:
	python3 -m venv .env
	pip install -r requirements.txt
	pip install -r dev_requirements.txt

test:
	mkdir -p coverage/html
	python3 -m coverage run tests/test_*.py
	python3 -m coverage report --show-missing
	python3 -m coverage xml -o coverage/coverage.xml
	python3 -m coverage html -d coverage/html/
	python3 -m coverage json -o coverage/coverage.json

docs:
	mkdir -p docs
	pydoc3 -w google_status
	mv google_status.html docs/index.html

build:
	python3 setup.py sdist
	python3 setup.py build
	docker build -t google_status:`cat VERSION` .

publish:
	echo "TOOD"

clean:
	python3 -m coverage erase
	rm -rf dist
	rm -rf docs
	rm -rf coverage
	rm -rf build
	docker ps -qa --filter "ancestor=google_status:$(cat VERSION)" | xargs --no-run-if-empty docker rm
	docker images -q --filter "reference=google_status:$(cat VERSION)" | xargs --no-run-if-empty docker rmi

all:
	make init-dev
	make tests
	make docs
	make build
	