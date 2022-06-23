all:
	python3 report_generator.py --iterate
	python3 pca_workload.py
	python3 distortion.py
	python3 kmean.py 6
post:
	python3 pca_workload_post.py
	python3 distortion.py
	python3 kmean_post.py 2
