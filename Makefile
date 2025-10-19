.DEFAULT_GOAL := test

test: test_down
	docker compose up
.PHONY: test

test_down:
	docker compose down
.PHONY: test_down

