.DEFAULT_GOAL := test

test: test_down
	docker compose watch
.PHONY: test

test_down:
	docker compose down
.PHONY: test_down

