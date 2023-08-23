notes.txt:
	gunzip notes.txt.gz

clean:
	rm -rf output
	rm -f 00*
	rm -f processed_files.txt
	#rm -f notes.txt
