all: execute
	ffmpeg -r 60 -i frames/frame_%04d.png -vcodec libx264 cell_division.mp4

execute:
	python3 src/main.py
