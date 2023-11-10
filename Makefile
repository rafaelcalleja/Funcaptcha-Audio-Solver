.EXPORT_ALL_VARIABLES:

DOCKER_BUILDKIT ?= 0

WHISPER_TAG ?= latest
WHISPER_IMAGE ?= onerahmet/openai-whisper-asr-webservice:$(WHISPER_TAG)
WHISPER_PORT ?= 9001

ASR_MODEL ?= tiny
ASR_ENGINE ?= openai_whisper

DOCKER_TAG ?= latest
DOCKER_IMAGE ?= rafaelcalleja/funcaptcha-solver:$(DOCKER_TAG)
PORT ?= 9000

SSH_CONTAINER ?= funcaptcha-solver-webservice
SSH_SHELL ?= /bin/bash

.PHONY: run
run:
	DOCKER_IMAGE=$(DOCKER_IMAGE) docker compose up -d --force-recreate

.PHONY: build
build:
	DOCKER_IMAGE=$(DOCKER_IMAGE) docker compose --env-file /dev/null build

.PHONY: stop
stop:
	docker compose down

destroy:
	DOCKER_IMAGE=$(DOCKER_IMAGE) docker compose down --rmi local -v
	docker rmi $(DOCKER_IMAGE)

.PHONY: logs
logs:
	docker compose logs -f

push:
	docker push $(DOCKER_IMAGE)

ssh:
	docker compose exec $(SSH_CONTAINER) $(SSH_SHELL)
