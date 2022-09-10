import time
import random
import terylene
from threading import Lock,Thread

terylene.curs_hide()

lock = Lock()

def task(y):
	bar = terylene.Bar(y,formats="[[#]] $rate$% $values$/$totalvalues$")
	for i in range(50):
		lock.acquire()
		bar + 2
		lock.release()
		time.sleep(random.random())

for i in range(10):
	Thread(target=task,args=(i,)).start()

# import time
# import terylene

# bar = terylene.Bar(0)

# for i in range(bar.totalvalues):
# 	bar + 1
# 	time.sleep(0.5)