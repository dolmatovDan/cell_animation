all:
	ffmpeg -r 60 -i frames/frame_%04d.png -vcodec libx264 cell_division.mp4
