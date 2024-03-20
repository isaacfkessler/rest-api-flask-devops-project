APP = restapi-devops

test:
	@pytest -v --disable-warnings
	@black .

compose:
	@docker compose build
	@docker compose up

heroku:
	@heroku container:login
	@heroku container:push -a $(APP) web
	@heroku container:release -a $(APP) web