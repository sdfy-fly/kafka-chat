DC = docker-compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .env
APP_FILE = docker/app.yaml
STORAGES_FILE = docker/storages.yaml
APP_CONTAINER = main-app


.PHONY: all
all:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} ${ENV} up --build -d


.PHONY: app
app:
	${DC} -f ${APP_FILE} ${ENV} up --build -d


.PHONY: storages
storages:
	${DC} -f ${STORAGES_FILE} ${ENV} up --build -d


.PHONY: app-shell
app-shell:
	${EXEC} ${APP_CONTAINER} bash


.PHONY: all-down
all-down:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} down


.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} down


.PHONY: storages-down
storages-down:
	${DC} -f ${STORAGES_FILE} down


.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f


.PHONY: tests
tests:
	${EXEC} ${APP_CONTAINER} pytest
