import random, time
import selenium

def send(object, mesg, wpm=700, random_fuzzing=0.1):
    cpm = wpm * 5
    time_per_char = float(60)/float(cpm)
    for char in mesg:
        time.sleep(time_per_char)
        object.send_keys(char)