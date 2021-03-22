tree:
	mkdir -p log data/in

build: tree
	docker-compose up

test-env:
	( \
		python3 -m venv venv; \
		source ./venv/bin/activate; \
		pip install -r requirements_test.txt; \
		deactivate; \
	)

test:
	( \
		source ./venv/bin/activate; \
		pytest -v; \
		deactivate; \
	)
