from phonePrice import main
from threading import Timer
import time

def schedule(t):
	while True:
		time.sleep(t)
		Timer(t,main).start()

schedule(2*60*60)
