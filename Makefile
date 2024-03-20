APP = restapi-devops

test:
	@pytest -v --disable-warnings
	@black .
	@bandit -r . -x '/.venv/','/tests/'

compose:
	@docker compose build
	@docker compose up

#heroku:
#	@heroku container:login
#	@heroku container:push -a $(APP) web
#	@heroku container:release -a $(APP) web

setup-dev:
	@kind create cluster --config kubernetes/config/config.yaml
	@kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
	@kubectl wait --namespace ingress-nginx \
  		--for=condition=ready pod \
  		--selector=app.kubernetes.io/component=controller \
  		--timeout=270s
	@helm upgrade \
	--install \
	--set image.tag=5.0.8 \
	--set auth.rootPassword="root" \
	mongodb kubernetes/charts/mongodb
	@kubectl wait \
  		--for=condition=ready pod \
  		--selector=app.kubernetes.io/component=mongodb \
  		--timeout=270s

teardown-dev:
	@kind delete clusters kind