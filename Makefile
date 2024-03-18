APP = restapi

test:
	@pytest -v --disable-warnings

compose:
	@docker compose build
	@docker compose up