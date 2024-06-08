.PHONY: build

build:
	@docker build -t gustavo/spark-base-hadoop ./cluster-hadoop/hadoop/spark-base
	@docker build -t gustavo/spark-master-hadoop ./cluster-hadoop/hadoop/spark-master
	@docker build -t gustavo/spark-worker-hadoop ./cluster-hadoop/hadoop/spark-worker
