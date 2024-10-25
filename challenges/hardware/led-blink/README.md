# Krusty Krab Heist

Plankton planning a heist to get his hands on the secret formula but he needs help getting in.
Karen did some scouting and found a smart speaker controlling the door along with an eeprom with some useful information on it.
Can you unlock the door by talking to the smart speaker with a laser.

```UMASS{tHe_5ecrEt_4mula}```

## Internal Info
This challenge uses a FAT12 file system on an eeprom with a wav file that has a 20 byte repeating XOR cipher (the key can be determined because the first 20 bytes of a wav file header are always known)

### Solve
There are 2 scripts needed. First, write a script to read some or all of the eeprom and dump it on uart so it can be downlaoded localy. Once downloaded, it is easy to see it is a FAT12 fs so you can mount it and find the XOR key. The second script needs to be able to read from the file system and output the intensities from the wav file on the laser (port c) at the specified sample rate.