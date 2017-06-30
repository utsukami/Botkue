xdotool mousemove 2880 625 && sleep 1s && xdotool click 1 && sleep 1s;
for x in $(xdotool search --name "Open File"); do 
	xdotool mousemove --window $x 500 100; 
	xdotool click 1; 
	xdotool mousemove --window $x 900 475;
	xdotool click 1;
 done
