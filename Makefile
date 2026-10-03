up:
	docker compose up --build

bench:
	python3 -m src.experiments.benchmark_suite

verify:
	python3 -m src.experiments.e1_arm_licensing
	python3 -m src.experiments.e2_digitization
	python3 -m src.experiments.e3_network
	python3 -m src.experiments.e4_trends
	python3 -m src.experiments.e5_selector
	cat data/live/benchmark_table.md
