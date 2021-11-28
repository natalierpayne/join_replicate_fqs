test:
	pytest -xv --pylint --flake8 test.py join_replicate_fqs.py

run_concat:
	./join_replicate_fqs.py _WR -f inputs/*.fq -co concat_dir

run_extract:
	./join_replicate_fqs.py _WR -f inputs/*.fq -ed extract_dir
