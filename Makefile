build:
	docker build -t rel_generator .

stage1: build
	rm -rf out/
	./run python stage1.py doclist

stage2: build
	./run python stage2.py