.PHONY: all

PROJECT_NAME=$(shell dirname ${PWD}/.|rev|cut -d\/ -f 1|rev)
DOCKER_HUB_ORG?=leopepe
DOCKER_IMG_NAME?=${PROJECT_NAME}
VERSION?=$(shell cat ${PROJECT_NAME}/__version__.py|cut -d\  -f3|sed 's/"//g'|sed 's/\ //g')

all: virtualenv install docker-push

virtualenv:
	virtualenv -p python3.6 venv/
	./venv/bin/python -m pip install -r requirements

install:
	./venv/bin/python setup.py install

docker-build:
	docker run --rm -v $(shell pwd):/worker -w /worker iron/python:3.5.1-dev pip install -t packages -r requirements
	docker build -t ${PROJECT_NAME}:${VERSION} .
	docker tag ${DOCKER_IMG_NAME}:${VERSION} ${DOCKER_HUB_ORG}/${DOCKER_IMG_NAME}:${VERSION}

docker-push-hub:
	docker tag ${DOCKER_IMG_NAME}:${VERSION} ${DOCKER_HUB_ORG}/${DOCKER_IMG_NAME}:${VERSION}
	docker push ${DOCKER_HUB_ORG}/${DOCKER_IMG_NAME}:${VERSION}

docker-push: docker-build docker-push-hub

test:
	docker run --rm -v $(shell pwd):/worker -e "PYTHONPATH=/worker/packages" -w /worker iron/python:3.5.1 python3 -m ${PROJECT_NAME}

clean:
	sudo rm -rf venv/*
	sudo rm -rf dist build
	sudo rm -rf ${PROJECT_NAME}.egg-info
	find . -name __pycache__ | xargs -I {} sudo rm -rf {}
	find . -name *.pyc |xargs -I {} sudo rm -rf {}
	sudo rm -rf packages
