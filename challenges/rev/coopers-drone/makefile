
all:
	nasm -f elf64 drone.asm -o drone.o
	ld drone.o -o ./static/drone
	rm drone.o
	strip ./static/drone

clean:
	rm ./static/drone