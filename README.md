# Terylene
The thing that make your terminal beautiful

# Example
A simple example
```python
import time,terylene

bar = terylene.Bar(0)

for i in range(bar.totalvalues):
	bar + 1
	time.sleep(0.5)
```

And a more difficult example
```python
import time,random,terylene
from threading import Lock,Thread

lock = Lock()
terylene.curs_hide()

def task(y):
	global lock
	bar = terylene.Bar(y,formats="[[#]] $rate$% $values$/$totalvalues$")
	for i in range(50):
		lock.acquire()
		bar + 2
		lock.release()
		time.sleep(random.random())

for i in range(10):
	Thread(target=task,args=(i,)).start()
```

# Afterwards
Enjoy it :smile: