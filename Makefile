up-build:
	./scripts/check_postgres.sh
	docker-compose up --build -d

test:
	docker-compose exec web pytest -s --cov

createsuperuser:
	docker-compose exec web python manage.py createsuperuser
