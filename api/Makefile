#	Make file not needed. 
#	Its purpose is to simplify commands for beginners.


clean:
	rm -rf **/__pycache__

code-format:
	black .

install:
	pip install -r requirements.txt

migrate:
	flask db migrate -d flaskr/database/migrations

migrate-revision:
	flask db revision -d flaskr/database/migrations

migration-upgrade:
	flask db upgrade -d flaskr/database/migrations

migration-downgrade:
	flask db downgrade -d flaskr/database/migrations

run:
	flask run --host=0.0.0.0 --debug

test:
	pytest -v --cov --cov-fail-under=100

test-report:
	pytest --cov-report html --cov .

all:
	make code-format
	make clean
	make install
	make migration-upgrade
	make test
	make run