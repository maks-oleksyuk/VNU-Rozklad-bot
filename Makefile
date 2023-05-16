include .env

.PHONY: up down stop prune ps shell logs db-dump

default: up

## help	:	Print commands help.
help : Makefile
	@sed -n 's/^##//p' $<

## up	:	Start up containers.
up:
	@echo "Starting up containers for for $(PROJECT_NAME)..."
	docker compose pull
	docker compose build
	docker compose up -d --remove-orphans

## build	:	Build python image.
build:
	@echo "Building python image for for $(PROJECT_NAME)..."
	docker compose build

## down	:	Stop containers.
down: stop

## start	:	Start containers without updating.
start:
	@echo "Starting containers for $(PROJECT_NAME) from where you left off..."
	@docker compose start

## stop	:	Stop containers.
stop:
	@echo "Stopping containers for $(PROJECT_NAME)..."
	@docker compose stop

## prune	:	Remove containers and their volumes.
##		You can optionally pass an argument with the service name to prune single container
##		prune mariadb	: Prune `mariadb` container and remove its volumes.
##		prune mariadb solr	: Prune `mariadb` and `solr` containers and remove their volumes.
prune:
	@echo "Removing containers for $(PROJECT_NAME)..."
	@docker compose down -v $(filter-out $@,$(MAKECMDGOALS))

## ps	:	List running containers.
ps:
	@docker ps --filter name='$(PROJECT_NAME)*'

## shell	:	Access `python` container via shell.
##		You can optionally pass an argument with a service name to open a shell on the specified container
shell:
	docker exec -ti -e COLUMNS=$(shell tput cols) -e LINES=$(shell tput lines) $(shell docker ps --filter name='$(PROJECT_NAME)_$(or $(filter-out $@,$(MAKECMDGOALS)), 'python')' --format "{{ .ID }}") sh

## logs	:	View containers logs.
##		You can optionally pass an argument with the service name to limit logs
##		logs bot	: View `python` container logs.
##		logs bot db	: View `python` and `database` containers logs.
logs:
	@docker compose logs -f $(filter-out $@,$(MAKECMDGOALS))

## db-dump:	Dump database to db/dump.
db-dump:
	if [ ! -d "db-dump" ]; then mkdir "db-dump"; fi
	@docker compose exec -t ${DB_HOST} mysqldump -u${DB_ROOT_USER} -p${DB_ROOT_PASS} ${DB_NAME} > db/dump/bot-db-dump_$(shell date +%F_%H:%M).sql

# https://stackoverflow.com/a/6273809/1826109
%:
	@: