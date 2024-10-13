release: 
	gcc tars.c -o tars
	patchelf --set-interpreter ./ld-linux-x86-64.so.2 --set-rpath . tars