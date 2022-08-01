########################################################################################################################
# Style
########################################################################################################################

.PHONY: pre_commit
pre_commit:
	pre-commit run --all-files


########################################################################################################################
# Rewrite
########################################################################################################################

.PHONY: build
build:
	poetry build

.PHONY: dev
dev: pre_commit build run

.PHONY: run
run:
	PYTHON_ENV=development \
	DD_ACTIVE=False \
	STATSD_HOST="192.168.1.175" \
	DD_AGENT_HOST="192.168.1.175" \
	DD_ENV="Tuxbot-dev" \
	CLUSTER_ID=1 \
	CLUSTER_COUNT=1 \
	SHARD_ID=0 \
	SHARD_COUNT=1 \
	FIRST_SHARD_ID=0 \
	LAST_SHARD_ID=0 \
	poetry run start
