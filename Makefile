APP = restapi

test:
	@pytest -v --disable-warnings

compose:
	@docker compose build
	@docker compose up

heroku:
	@heroku container:login
	@heroku container:push -a restapi-devops web
	@heroku container:release -a restapi-devops web