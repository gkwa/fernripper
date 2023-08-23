run: notes.txt
	python3 main.py notes.txt '^\* '

notes.txt:
	gunzip --keep notes.txt.gz

clean:
	rm -rf output
	rm -f processed_files.txt
	#rm -f notes.txt
