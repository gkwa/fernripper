run2: notes.txt
	python3 main.py --output_dir output/test2 notes.txt '^\** '

run1: notes.txt
	python3 main.py --output_dir output/test1 notes.txt '^\* '

notes.txt:
	gunzip --keep notes.txt.gz

clean:
	rm -rf output
	rm -f processed_files.txt
	#rm -f notes.txt
